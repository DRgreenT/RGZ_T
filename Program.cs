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
        var subjectMap = AnalyzeClassifications(classifications);
        CleanSubjectMap(subjectMap);
        SaveResults(subjectMap);
    }

    static List<Classification> LoadCsv(string path)
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
            var record = new Classification
            {
                AnnotationsJson = csv.GetField("annotations"),
                SubjectDataJson = csv.GetField("subject_data"),
                SubjectId = long.TryParse(csv.GetField("subject_ids"), out var sid) ? sid : 0
            };

            records.Add(record);
        }

        Console.WriteLine($"Loaded {records.Count} records.");
        return records;
    }

    static Dictionary<string, Subject> AnalyzeClassifications(List<Classification> classifications)
    {
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
                        subjectMap[key] = subject;

                    if (record.Annotations != null)
                    {
                        foreach (var annotation in record.Annotations)
                        {
                            if (!subject.TaskData.ContainsKey(annotation.Task))
                                subject.TaskData[annotation.Task] = new();

                            if (annotation.Value.ValueKind == JsonValueKind.String)
                            {
                                var str = annotation.Value.GetString();
                                if (!string.IsNullOrWhiteSpace(str))
                                    subject.TaskData[annotation.Task].Add(annotation.Value);
                            }
                            else if (annotation.Value.ValueKind == JsonValueKind.Array)
                            {
                                foreach (var item in annotation.Value.EnumerateArray())
                                    subject.TaskData[annotation.Task].Add(item);
                            }
                        }
                    }

                    // Convert TaskData into structured output
                    foreach (var task in subject.TaskData)
                    {
                        if (task.Key == "T1")
                        {
                            foreach (var labelElement in task.Value)
                            {
                                if (labelElement.ValueKind == JsonValueKind.String)
                                {
                                    string label = labelElement.GetString() ?? "(blank)";
                                    if (!subject.T1LabelCounts.ContainsKey(label))
                                        subject.T1LabelCounts[label] = 0;
                                    subject.T1LabelCounts[label]++;
                                }
                            }
                        }
                        else
                        {
                            if (!subject.Tasks.ContainsKey(task.Key))
                                subject.Tasks[task.Key] = new();

                            foreach (var entry in task.Value)
                            {
                                try
                                {
                                    if (entry.ValueKind == JsonValueKind.Object)
                                    {
                                        var toolLabel = entry.GetProperty("tool_label").GetString() ?? "unknown";
                                        var value = new TaskValue
                                        {
                                            X = entry.GetProperty("x").GetDouble(),
                                            Y = entry.GetProperty("y").GetDouble(),
                                            Tool = entry.GetProperty("tool").GetInt32(),
                                            Frame = entry.GetProperty("frame").GetInt32(),
                                            Width = entry.TryGetProperty("width", out var w) ? w.GetDouble() : null,
                                            Height = entry.TryGetProperty("height", out var h) ? h.GetDouble() : null,
                                        };

                                        if (!subject.Tasks[task.Key].ContainsKey(toolLabel))
                                            subject.Tasks[task.Key][toolLabel] = new();

                                        subject.Tasks[task.Key][toolLabel].Add(value);
                                    }
                                }
                                catch (Exception ex)
                                {
                                    Console.WriteLine($"Failed to parse task item: {ex.Message}");
                                }
                            }
                        }
                    }
                }
            }
        }

        return subjectMap;
    }

    static void CleanSubjectMap(Dictionary<string, Subject> subjectMap)
    {
        var keysToRemove = new List<string>();

        foreach (var kvp in subjectMap)
        {
            var subject = kvp.Value;

            if (string.IsNullOrWhiteSpace(subject.SubjectID))
            {
                keysToRemove.Add(kvp.Key);
                continue;
            }

            bool hasValidTasks = subject.Tasks != null && subject.Tasks.Any(kvp => string.Compare(kvp.Key, "T0") >= 0 && kvp.Value.Count > 0);

            if (!hasValidTasks)
            {
                keysToRemove.Add(kvp.Key);
                continue;
            }
        }

        foreach (var key in keysToRemove)
        {
            subjectMap.Remove(key);
        }

        Console.WriteLine($"Filtered to {subjectMap.Count} valid subjects.");
    }

    static void SaveResults(Dictionary<string, Subject> subjectMap)
    {
        var json = JsonSerializer.Serialize(subjectMap, new JsonSerializerOptions { WriteIndented = true });
        File.WriteAllText("subjects_output.json", json);
        Console.WriteLine("Results have been saved as JSON.");
    }
}
