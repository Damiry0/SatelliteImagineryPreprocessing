

int[,,,] GlcmMatrix(int[,] image, int vmin, int vmax, int levels, int[] distances, int[] angles)
{
    int[,,,] glcm = new int[levels, levels, distances.Length, angles.Length];

    var h = image.GetLength(0);
    var w = image.GetLength(1);
    var count = 0;

    for (int angleLen = 0; angleLen<angles.Length; angleLen++)
    {
        for (int distanceLen = 0; distanceLen<angles.Length; distanceLen++)
        {
            var offset_row = Math.Ceiling(Math.Sin(angles[angleLen] * distances[distanceLen]));
            var offset_col = Math.Ceiling(Math.Cos(angles[angleLen] * distances[distanceLen]));
            var start_row = Math.Max(0, -offset_row);
            var end_row = Math.Min(h, h - offset_row);
            var start_col = Math.Max(0, -offset_col);
            var end_col = Math.Min(w, w - offset_col);
            IEnumerable<int> x = Enumerable.Range((int)start_row, (int)end_row);
            IEnumerable<int> y = Enumerable.Range((int)start_col, (int)end_col);
            var watch = System.Diagnostics.Stopwatch.StartNew();

            for (var i = 0; i < levels; i++)
            {
                for (var j = 0; j < levels; j++)
                {
                    foreach (var xVar in x)
                    {
                        foreach (var yVar in y)
                        {
                            
                            var dx = xVar + (int)offset_row;
                            var dy = yVar + (int)offset_col;
                            if (image[xVar, yVar] == i && image[dx, dy] == j)
                            {
                                glcm[i, j, angleLen, distanceLen] += 1;
                            }
                        }
                    }

                }
            }
            watch.Stop();
            var elapsedMs = watch.ElapsedMilliseconds;
            Console.WriteLine("Time elapsed : ");
            Console.WriteLine(elapsedMs);
        }
    }

    return glcm;
}

int[,,,] ParallelGlcmMatrix(int[,] image, int vmin, int vmax, int levels, int[] distances, int[] angles, int proc_count)
{
    var watch = System.Diagnostics.Stopwatch.StartNew();
    int[,,,] glcm = new int[levels, levels, distances.Length, angles.Length];

    var h = image.GetLength(0);
    var w = image.GetLength(1);
    var count = 0;

    for (int angleLen = 0; angleLen<angles.Length; angleLen++)
    {
        for (int distanceLen = 0; distanceLen<angles.Length; distanceLen++)
        {
            var offset_row = Math.Ceiling(Math.Sin(angles[angleLen] * distances[distanceLen]));
            var offset_col = Math.Ceiling(Math.Cos(angles[angleLen] * distances[distanceLen]));
            var start_row = Math.Max(0, -offset_row);
            var end_row = Math.Min(h, h - offset_row);
            var start_col = Math.Max(0, -offset_col);
            var end_col = Math.Min(w, w - offset_col);
            IEnumerable<int> x = Enumerable.Range((int)start_row, (int)end_row);
            IEnumerable<int> y = Enumerable.Range((int)start_col, (int)end_col);
            
            ParallelOptions parallelOptions = new ParallelOptions
            {
                MaxDegreeOfParallelism = proc_count
            };
            
            

            Parallel.For(0, levels, parallelOptions, i =>
            {
                for (var j = 0; j < levels; j++)
                {
                    foreach (var xVar in x)
                    {
                        foreach (var yVar in y)
                        {
                            
                            var dx = xVar + (int)offset_row;
                            var dy = yVar + (int)offset_col;
                            if (image[xVar, yVar] == i && image[dx, dy] == j)
                            {
                                glcm[i, j, angleLen, distanceLen] += 1;
                            }
                        }
                    }

                }
            });
            watch.Stop();
            var elapsedMs = watch.ElapsedMilliseconds;
            Console.WriteLine($"Time elapsed : {elapsedMs} , Processor count : {proc_count}");
        }
    }

    return glcm;
}


int[,] LoadTxt(string filePath)
{
    string[] lines = File.ReadAllLines(filePath);

    int numRows = lines.Length;
    int numCols = lines[0].Split(' ').Length;

    int[,] data = new int[numRows, numCols];

    for (int i = 0; i < numRows; i++)
    {
        string[] values = lines[i].Split(' ');

        for (int j = 0; j < numCols; j++)
        {
            if (double.TryParse(values[j], out double value))
            {
                data[i, j] = (int) value;
            }
            else
            {
                // Handle parsing error if needed.
            }
        }
    }

    return data;
}

var workingDirectory = Environment.CurrentDirectory;
var projectDirectory = Directory.GetParent(workingDirectory).Parent.Parent.FullName;

Console.WriteLine("The number of processors " +
                  "on this computer is .");
Console.WriteLine(Environment.ProcessorCount);

var file_path = projectDirectory + @"\image_small.txt";
int[,] data = LoadTxt(file_path);
int[] processors = { 1, 2, 3, 4, 5, 8, 16, 32 };
int[] distances = { 1 };
int[] angles = { 0 };

foreach (var proc in processors)
{
    var result1 = ParallelGlcmMatrix(data, 0, 8, 32, distances, angles, proc);    
}

