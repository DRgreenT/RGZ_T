using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
using System.Text.Json;
using RGZ_T.Models;
class Program
{
    static void Main(string[] args)
    {
        var classifications = LoadCsv("radio-galaxy-zoo-emu-classifications.csv");
        Dictionary<string, Subject> subjectMap = new();

        foreach (var record in classifications)
        {
            if (record.SubjectData != null)
            {
                foreach (var kvp in record.SubjectData)
                {
                    string key = kvp.Key;
                    Subject subject = kvp.Value;

                    if (!subjectMap.TryGetValue(key, out var existing))
                    {
                        subjectMap[key] = subject;
                    }

                    if (record.Annotations != null)
                    {
                        foreach (var annotation in record.Annotations)
                        {
                            if (!subjectMap[key].TaskData.ContainsKey(annotation.Task))
                            {
                                subjectMap[key].TaskData[annotation.Task] = new List<JsonElement>();
                                subjectMap[key].TaskValueStrings[annotation.Task] = new List<string>();
                            }

                            if (annotation.Value.ValueKind == JsonValueKind.String)
                            {
                                var str = annotation.Value.GetString();
                                if (!string.IsNullOrWhiteSpace(str))
                                {
                                    subjectMap[key].TaskData[annotation.Task].Add(annotation.Value);
                                    subjectMap[key].TaskValueStrings[annotation.Task].Add(str);
                                }
                            }
                            else if (annotation.Value.ValueKind == JsonValueKind.Array)
                            {
                                foreach (var item in annotation.Value.EnumerateArray())
                                {
                                    subjectMap[key].TaskData[annotation.Task].Add(item);
                                }
                            }
                        }
                    }
                }
            }
        }

        foreach (var kvp in subjectMap)
        {
            var s = kvp.Value;
            Console.WriteLine($"Subject [{kvp.Key}]:  SubjectID={s.SubjectID}");
            foreach (var task in s.TaskData)
            {
                Console.WriteLine($"  Task: {task.Key} (Entries: {task.Value.Count})");
                foreach (var val in task.Value)
                {
                    Console.WriteLine($"    ␦ {val}");
                }
                if (s.TaskValueStrings.ContainsKey(task.Key))
                {
                    foreach (var val in s.TaskValueStrings[task.Key])
                    {
                        Console.WriteLine($"    ↪ {val}");
                    }
                }
            }
        }
    }

    public static List<Classification> LoadCsv(string path)
    {
        using var reader = new StreamReader(path);
        using var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true,
            BadDataFound = context => Console.WriteLine($"Bad data: {context.RawRecord}"),
            MissingFieldFound = null
        });

        var records = new List<Classification>();

        csv.Read();
        csv.ReadHeader();
        while (csv.Read())
        {
            var dateStr = csv.GetField("created_at").Replace(" UTC", "").Trim();
            var userIdStr = csv.GetField("user_id");
            long userId = long.TryParse(userIdStr, out var uid) ? uid : 0;

            var record = new Classification
            {
                ClassificationId = csv.GetField<long>("classification_id"),
                UserName = csv.GetField("user_name"),
                UserId = userId,
                UserIP = csv.GetField("user_ip"),
                WorkflowId = csv.GetField<long>("workflow_id"),
                WorkflowName = csv.GetField("workflow_name"),
                WorkflowVersion = csv.GetField("workflow_version"),
                CreatedAt = DateTime.ParseExact(dateStr, "yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture),
                MetadataJson = csv.GetField("metadata"),
                AnnotationsJson = csv.GetField("annotations"),
                SubjectDataJson = csv.GetField("subject_data"),
                SubjectId = long.TryParse(csv.GetField("subject_ids"), out var sid) ? sid : 0
            };

            records.Add(record);
        }

        Console.WriteLine($"Loaded {records.Count} records.");
        return records;
    }
}
