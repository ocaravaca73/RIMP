using System.Text.Json;
using System.Text.Json.Serialization;
using System.Diagnostics;
using System.Text;

// RIMP Injector: reads a TaskSpec JSON, ensures projects/solution exist,
// generates source/test files from templates, and writes plan/manifest.txt.
// Safe/idempotent: re-writes files only if content changes.

internal sealed class TaskSpec
{
    public string WorkItemId { get; set; } = "";
    public string FeatureBranch { get; set; } = "";
    public List<string> ProjectsToEnsure { get; set; } = new();
    public List<FileSpec> Files { get; set; } = new();
    public List<TestSpec> Tests { get; set; } = new();
    public string CommitMessage { get; set; } = "auto-inject";
}

internal sealed class FileSpec
{
    public string Path { get; set; } = "";
    public string Template { get; set; } = "";
}

internal sealed class TestSpec : FileSpec
{
    public Dictionary<string, string>? Data { get; set; }
}

internal static class Program
{
    private static int Main(string[] args)
    {
        // Args
        var taskspecPath = GetArg(args, "--taskspec") ?? "plan/taskspec.json";
        var dryRun = (GetArg(args, "--dry-run") ?? "false").Equals("true", StringComparison.OrdinalIgnoreCase);

        var repoRoot = Directory.GetCurrentDirectory();
        var manifestPath = Path.Combine(repoRoot, "plan", "manifest.txt");
        Directory.CreateDirectory(Path.GetDirectoryName(manifestPath)!);

        Console.WriteLine($"[Injector] RepoRoot={repoRoot}");
        Console.WriteLine($"[Injector] TaskSpec={taskspecPath}; DryRun={dryRun}");

        // Read TaskSpec
        if (!File.Exists(taskspecPath))
        {
            Console.Error.WriteLine($"[Injector] TaskSpec not found: {taskspecPath}");
            return 2;
        }

        var json = File.ReadAllText(taskspecPath, Encoding.UTF8);
        var spec = JsonSerializer.Deserialize<TaskSpec>(json, new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            ReadCommentHandling = JsonCommentHandling.Skip,
            AllowTrailingCommas = true
        }) ?? new TaskSpec();

        var touched = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        // Ensure projects (and create solution if missing)
        EnsureProjectsAndSolution(repoRoot, spec, touched);

        // Generate files from templates
        foreach (var f in spec.Files)
            GenerateFromTemplate(repoRoot, f.Path, f.Template, null, touched);

        foreach (var t in spec.Tests)
            GenerateFromTemplate(repoRoot, t.Path, t.Template, t.Data, touched);

        // Write manifest
        File.WriteAllLines(manifestPath, touched.OrderBy(p => p));
        Console.WriteLine($"[Injector] Manifest written: {manifestPath}");
        return 0;
    }

    private static void EnsureProjectsAndSolution(string repoRoot, TaskSpec spec, HashSet<string> touched)
    {
        // Create solution if not present
        var slnPath = Path.Combine(repoRoot, "RIMP.sln");
        if (!File.Exists(slnPath))
        {
            Run("dotnet", "new sln -n RIMP", repoRoot);
            Console.WriteLine("[Injector] Created solution RIMP.sln");
        }

        foreach (var csprojRel in spec.ProjectsToEnsure.Distinct(StringComparer.OrdinalIgnoreCase))
        {
            var csprojPath = Path.Combine(repoRoot, csprojRel.Replace('/', Path.DirectorySeparatorChar));
            var dir = Path.GetDirectoryName(csprojPath)!;
            Directory.CreateDirectory(dir);

            var isTest = csprojRel.Contains(".Tests", StringComparison.OrdinalIgnoreCase) ||
                         csprojRel.Contains("/Tests/", StringComparison.OrdinalIgnoreCase) ||
                         csprojRel.Contains("\\Tests\\", StringComparison.OrdinalIgnoreCase);

            if (!File.Exists(csprojPath))
            {
                if (isTest)
                {
                    // Test project (xUnit)
                    var content = TestCsprojTemplate(GetRelativePath(dir, repoRoot));
                    File.WriteAllText(csprojPath, content, Encoding.UTF8);
                }
                else
                {
                    // Class library
                    var content = ClassLibCsprojTemplate();
                    File.WriteAllText(csprojPath, content, Encoding.UTF8);
                }
                touched.Add(csprojRel);
                Console.WriteLine($"[Injector] Created project: {csprojRel}");
            }

            // Add to solution if not already
            // dotnet sln list → check presence is cumbersome; we can try add and ignore error if already added
            Run("dotnet", $"sln RIMP.sln add \"{csprojPath}\"", repoRoot, ignoreErrors: true);
        }

        // If we created a test project, try to add ProjectReference automatically
        var testProj = spec.ProjectsToEnsure.FirstOrDefault(p => p.Contains(".Tests", StringComparison.OrdinalIgnoreCase));
        if (!string.IsNullOrEmpty(testProj))
        {
            var mainProjGuess = GuessMainProject(spec);
            if (mainProjGuess is not null)
            {
                var testProjPath = Path.Combine(repoRoot, testProj.Replace('/', Path.DirectorySeparatorChar));
                var mainProjPath = Path.Combine(repoRoot, mainProjGuess.Replace('/', Path.DirectorySeparatorChar));
                TryAddProjectReference(testProjPath, mainProjPath);
                touched.Add(testProj);
            }
        }
    }

    private static string? GuessMainProject(TaskSpec spec)
    {
        // Heuristic: if there is a file under src/<Name>/..., infer project src/<Name>/<Name>.csproj
        var srcFile = spec.Files.Select(f => f.Path)
            .FirstOrDefault(p => p.StartsWith("src/", StringComparison.OrdinalIgnoreCase));
        if (srcFile is null) return null;

        // src/RIMP.Analytics/LapTimeAnalyzer.cs -> src/RIMP.Analytics/RIMP.Analytics.csproj
        var parts = srcFile.Split('/', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length < 2) return null;
        var projDir = $"src/{parts[1]}";
        var projName = parts[1];
        return $"{projDir}/{projName}.csproj";
    }

    private static void TryAddProjectReference(string testProjPath, string mainProjPath)
    {
        if (!File.Exists(testProjPath) || !File.Exists(mainProjPath)) return;
        // Read test csproj; if no ProjectReference to main, add it.
        var xml = File.ReadAllText(testProjPath, Encoding.UTF8);
        if (xml.Contains("<ProjectReference", StringComparison.OrdinalIgnoreCase) &&
            xml.Contains(Path.GetFileName(mainProjPath), StringComparison.OrdinalIgnoreCase))
            return;

        // Insert simple ItemGroup with ProjectReference
        var rel = GetRelativePath(Path.GetDirectoryName(testProjPath)!, mainProjPath);
        var insert = $@"
  <ItemGroup>
    <ProjectReference Include=""{rel}"" />
  </ItemGroup>
</Project>";
        xml = xml.Replace("</Project>", insert);
        File.WriteAllText(testProjPath, xml, Encoding.UTF8);
        Console.WriteLine($"[Injector] Added ProjectReference to {rel}");
    }

    private static void GenerateFromTemplate(string repoRoot, string targetRel, string templateName, Dictionary<string, string>? data, HashSet<string> touched)
    {
        if (string.IsNullOrWhiteSpace(targetRel))
            throw new ArgumentException("File path is required in TaskSpec.");
        if (string.IsNullOrWhiteSpace(templateName))
            throw new ArgumentException("Template name is required in TaskSpec.");

        var outPath = Path.Combine(repoRoot, targetRel.Replace('/', Path.DirectorySeparatorChar));
        Directory.CreateDirectory(Path.GetDirectoryName(outPath)!);

        var templatePath = Path.Combine(AppContext.BaseDirectory, "Templates", $"{templateName}.cs.txt");
        if (!File.Exists(templatePath))
            throw new FileNotFoundException($"Template not found: {templatePath}");

        var content = File.ReadAllText(templatePath, Encoding.UTF8);
        if (data is not null)
        {
            foreach (var kv in data)
                content = content.Replace("{{" + kv.Key + "}}", kv.Value);
        }

        var write = true;
        if (File.Exists(outPath))
        {
            var existing = File.ReadAllText(outPath, Encoding.UTF8);
            write = existing != content;
        }

        if (write)
        {
            File.WriteAllText(outPath, content, Encoding.UTF8);
            Console.WriteLine($"[Injector] Wrote: {targetRel}");
        }
        else
        {
            Console.WriteLine($"[Injector] Unchanged: {targetRel}");
        }

        touched.Add(targetRel.Replace('\\', '/'));
    }

    private static void Run(string fileName, string args, string workingDir, bool ignoreErrors = false)
    {
        var psi = new ProcessStartInfo(fileName, args)
        {
            WorkingDirectory = workingDir,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        };
        var p = Process.Start(psi)!;
        p.WaitForExit();
        if (p.ExitCode != 0 && !ignoreErrors)
        {
            Console.Error.WriteLine($"[Injector] Command failed: {fileName} {args}\n{p.StandardError.ReadToEnd()}");
            throw new Exception($"Command failed: {fileName} {args}");
        }
    }

    private static string? GetArg(string[] args, string name)
    {
        for (int i = 0; i < args.Length; i++)
        {
            if (string.Equals(args[i], name, StringComparison.OrdinalIgnoreCase))
                return (i + 1) < args.Length ? args[i + 1] : null;
        }
        return null;
    }

    private static string ClassLibCsprojTemplate() => """
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
""";

    private static string TestCsprojTemplate(string testProjDirRelToRepoRoot) => """
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.10.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.6" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>
  <!-- ProjectReference se añade automáticamente si se detecta el proyecto principal -->
</Project>
""";

    private static string GetRelativePath(string fromDir, string toPath)
    {
        var fromUri = new Uri(AppendDirectorySeparatorChar(fromDir));
        var toUri = new Uri(toPath);
        return Uri.UnescapeDataString(fromUri.MakeRelativeUri(toUri).ToString().Replace('/', Path.DirectorySeparatorChar));
    }

    private static string AppendDirectorySeparatorChar(string path)
        => path.EndsWith(Path.DirectorySeparatorChar) ? path : path + Path.DirectorySeparatorChar;
}
