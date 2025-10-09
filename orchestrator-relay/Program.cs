// Program.cs — classic entry point for Azure Functions Isolated
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace Rimp.Orchestrator.Relay
{
    public static class Program
    {
        public static async Task Main()
        {
            var host = new HostBuilder()
                .ConfigureFunctionsWorkerDefaults()
                .ConfigureServices(s =>
                {
                    // HttpClient used by the relay to call GitHub
                    s.AddHttpClient("github");
                })
                .Build();

            await host.RunAsync();
        }
    }
}

