using System.Net;
using System.Net.Http;                 // <-- Added in version 2
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;          // <-- Added in versión 2
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;


namespace Rimp.Orchestrator.Relay;

public class OrchestratorRelay
{
    private readonly ILogger _log;
    private readonly IHttpClientFactory _http;

    public OrchestratorRelay(ILoggerFactory lf, IHttpClientFactory http) { _log = lf.CreateLogger<OrchestratorRelay>(); _http = http; }

    [Function("OrchestratorRelay")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "rimp/orch/relay")] HttpRequestData req)
    {
        // Basic Auth
        if (!req.Headers.TryGetValues("Authorization", out var auth)) return Unauthorized(req);
        var userExp = Environment.GetEnvironmentVariable("HOOK_USER") ?? "";
        var passExp = Environment.GetEnvironmentVariable("HOOK_SECRET") ?? "";
        var h = auth.FirstOrDefault() ?? "";
        if (!h.StartsWith("Basic ", StringComparison.OrdinalIgnoreCase)) return Unauthorized(req);
        var raw = Encoding.UTF8.GetString(Convert.FromBase64String(h["Basic ".Length..]));
        var p = raw.IndexOf(':'); if (p < 0) return Unauthorized(req);
        if (!CtEq(raw[..p], userExp) || !CtEq(raw[(p + 1)..], passExp)) return Unauthorized(req);

        using var rd = new StreamReader(req.Body); var body = await rd.ReadToEndAsync();
        using var doc = JsonDocument.Parse(body); var root = doc.RootElement;

        string wi   = root.GetProperty("resource").GetProperty("id").GetInt32().ToString();
        string act  = root.TryGetProperty("eventType", out var ev) ? ev.GetString() ?? "workitem.updated" : "workitem.updated";
        string proj = root.GetProperty("resource").GetProperty("fields").GetProperty("System.TeamProject").GetString() ?? "";
        string st   = root.GetProperty("resource").GetProperty("fields").GetProperty("System.State").GetString() ?? "";
        string tags = root.GetProperty("resource").GetProperty("fields").TryGetProperty("System.Tags", out var t) ? (t.GetString() ?? "") : "";

        var dispatch = new {
            event_type = Environment.GetEnvironmentVariable("DISPATCH_EVENT") ?? "rimp.orch.updated",
            client_payload = new { workItemId = wi, action = act, project = proj, state = st, tags }
        };

        var owner = Environment.GetEnvironmentVariable("GH_OWNER")!;
        var repo  = Environment.GetEnvironmentVariable("GH_REPO")!;
        var pat   = Environment.GetEnvironmentVariable("GH_PAT")!;

        var http = _http.CreateClient("github");
        http.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("rimp-orch-relay","1.0"));
        http.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", pat);
        http.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/vnd.github+json"));
        http.DefaultRequestHeaders.Add("X-GitHub-Api-Version","2022-11-28");

        var url = $"https://api.github.com/repos/{owner}/{repo}/dispatches";
        var content = new StringContent(JsonSerializer.Serialize(dispatch), Encoding.UTF8, "application/json");
        var gh = await http.PostAsync(url, content);

        var resp = req.CreateResponse(gh.IsSuccessStatusCode ? HttpStatusCode.OK : gh.StatusCode);
        await resp.WriteStringAsync(gh.IsSuccessStatusCode ? "Dispatched" : "GitHub error");
        return resp;
    }

    private static bool CtEq(string a, string b) { if (a.Length != b.Length) return false; var d=0; for (int i=0;i<a.Length;i++) d |= a[i]^b[i]; return d==0; }
    private HttpResponseData Unauthorized(HttpRequestData req) { var r = req.CreateResponse(HttpStatusCode.Unauthorized); r.Headers.Add("WWW-Authenticate","Basic realm=\"RIMP-ORCH\""); return r; }
}
