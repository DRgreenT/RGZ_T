using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace RGZ_T.Models
{
    public class Annotation
    {
        [JsonPropertyName("task")]
        public string Task { get; set; } = string.Empty;

        [JsonPropertyName("task_label")]
        public string TaskLabel { get; set; } = string.Empty;

        [JsonPropertyName("value")]
        public JsonElement Value { get; set; }
    }
}
