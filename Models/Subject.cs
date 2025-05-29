using System.Text.Json;
using System.Text.Json.Serialization;


namespace RGZ_T.Models
{
    public class Subject
    {
        [JsonPropertyName("Filename")]
        public string? Filename { get; set; }

        [JsonPropertyName("RA")]
        public string? RA { get; set; }

        [JsonPropertyName("DEC")]
        public string? DEC { get; set; }

        [JsonPropertyName("subject ID")]
        public string? SubjectID { get; set; }

        public Dictionary<string, List<JsonElement>> TaskData { get; set; } = new();
        public Dictionary<string, List<string>> TaskValueStrings { get; set; } = new();
    }
}
