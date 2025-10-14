using System.Diagnostics;
using System.Text;

// RIMP CommitPush: commit & push files listed in a manifest to a target branch.
// Uses git CLI (Actions runner). Falls back to 'git add -A' if manifest missing/empty.

internal static class Program
{
    private static int Main(string[] args)
    {
        var branch = GetArg(args, "--branch") ?? throw new ArgumentException("--branch is required");
        var message = GetArg(args, "--message") ?? "auto-commit";
        var manifest = GetArg(args, "--manifest") ?? "plan/manifest.txt";

        var repoRoot = Directory.GetCurrentDirectory();
        Console.WriteLine($"[CommitPush] Branch={branch} | Manifest={manifest}");

        // Ensure we are on the target branch
        Run("git", $"switch {Escape(branch)}", repoRoot, ignoreErrors: false);

        // Stage changes
        var files = ReadManifest(manifest);
        if (files.Count == 0)
        {
            Console.WriteLine("[CommitPush] Manifest empty or not found. Falling back to git add -A.");
            Run("git", "add -A", repoRoot, ignoreErrors: false);
        }
        else
        {
            foreach (var f in files)
            {
                var p = f.Replace('/', Path.DirectorySeparatorChar);
                Run("git", $"add {Escape(p)}", repoRoot, ignoreErrors: false);
            }
        }

        // Commit (skip if nothing to commit)
        Run("git", "config user.email \"rimp-bot@users.noreply.github.com\"", repoRoot, true);
        Run("git", "config user.name \"rimp-bot\"", repoRoot, true);

        var commitExit = Run("git", $"commit -m {Escape(message)}", repoRoot, ignoreErrors: true);
        if (commitExit != 0)
        {
            Console.WriteLine("[CommitPush] Nothing to commit (working tree clean).");
        }

        // Push
        Run("git", $"push origin {Escape(branch)}", repoRoot, ignoreErrors: false);
        Console.WriteLine("[CommitPush] Push done.");
        return 0;
    }

    private static List<string> ReadManifest(string path)
    {
        try
        {
            if (!File.Exists(path)) return new List<string>();
            return File.ReadAllLines(path)
                       .Select(l => l.Trim())
                       .Where(l => !string.IsNullOrWhiteSpace(l))
                       .Distinct(StringComparer.OrdinalIgnoreCase)
                       .ToList();
        }
        catch { return new List<string>(); }
    }

    private static int Run(string fileName, string args, string cwd, bool ignoreErrors)
    {
        var psi = new ProcessStartInfo(fileName, args)
        {
            WorkingDirectory = cwd,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        };
        var p = Process.Start(psi)!;
        p.WaitForExit();
        if (p.ExitCode != 0 && !ignoreErrors)
        {
            Console.Error.WriteLine($"[CommitPush] Failed: {fileName} {args}\n{p.StandardError.ReadToEnd()}");
            throw new Exception($"Command failed: {fileName} {args}");
        }
        return p.ExitCode;
    }

    private static string Escape(string value)
        => "\"" + value.Replace("\"", "\\\"") + "\"";

    private static string? GetArg(string[] args, string name)
    {
        for (int i = 0; i < args.Length; i++)
            if (string.Equals(args[i], name, StringComparison.OrdinalIgnoreCase))
                return (i + 1) < args.Length ? args[i + 1] : null;
        return null;
    }
}
