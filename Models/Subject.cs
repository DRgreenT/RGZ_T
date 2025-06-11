using System.Text.Json;
using System.Text.Json.Serialization;


namespace RGZ_T.Models
{
    // Represents a subject being classified
    public class Subject
    {
        [JsonPropertyName("subject ID")]
        public string? SubjectID { get; set; }

        [JsonIgnore] // Do not export raw task data
        public Dictionary<string, List<JsonElement>> TaskData { get; set; } = new();

        // Parsed and structured task data by tool label (T0, T2, T3, etc.)
        public Dictionary<string, Dictionary<string, List<TaskValue>>> Tasks { get; set; } = new();

        // Special handling for T1 strings: label -> count
        public Dictionary<string, int> T1LabelCounts { get; set; } = new();
    }
}
