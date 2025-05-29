using System.Text.Json;

namespace RGZ_T.Models
{
    public class Classification
    {
        public long ClassificationId { get; set; }
        public string UserName { get; set; } = string.Empty;
        public long UserId { get; set; }
        public string UserIP { get; set; } = string.Empty;
        public long WorkflowId { get; set; }
        public string WorkflowName { get; set; } = string.Empty;
        public string WorkflowVersion { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; }
        public string MetadataJson { get; set; } = string.Empty;
        public string AnnotationsJson { get; set; } = string.Empty;
        public string SubjectDataJson { get; set; } = string.Empty;
        public long SubjectId { get; set; }

        public Dictionary<string, object>? Metadata => JsonSerializer.Deserialize<Dictionary<string, object>>(MetadataJson);
        public List<Annotation>? Annotations => JsonSerializer.Deserialize<List<Annotation>>(AnnotationsJson);
        public Dictionary<string, Subject>? SubjectData => JsonSerializer.Deserialize<Dictionary<string, Subject>>(SubjectDataJson);
    }
}
