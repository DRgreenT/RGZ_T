using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RGZ_T.Models
{
    // Represents a structured value extracted from a tool annotation
    public class TaskValue
    {
        public double X { get; set; }
        public double Y { get; set; }
        public int Tool { get; set; }
        public int Frame { get; set; }
        public double? Width { get; set; }
        public double? Height { get; set; }
    }
}
