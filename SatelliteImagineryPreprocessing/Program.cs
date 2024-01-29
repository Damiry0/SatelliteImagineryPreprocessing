

int[,,,] GlcmMatrix(int[,] image, int vmin, int vmax, int levels, int[] distances, int[] angles)
{
    int[,,,] glcm = new int[levels, levels, distances.Length, angles.Length];

    var h = image.GetLength(0);
    var w = image.GetLength(1);

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

var file_path = projectDirectory + @"\image.txt";
int[,] data = LoadTxt(file_path);
// int[,] numbers = { {1, 1, 5, 6, 8, 8}, 
//     {2, 3, 5, 7, 0, 2},
//     {0, 2, 3, 5, 6, 7}};
int[] distances = { 1 };
int[] angles = { 0 };


var result = GlcmMatrix(data, 0, 8, 9, distances, angles);

int dim1 = result.GetLength(0);
int dim2 = result.GetLength(1);


for (int i = 0; i < dim1; i++)
{
    for (int j = 0; j < dim2; j++)
    {
        Console.Write(result[i, j, 0, 0] + " ");
    }
    Console.WriteLine(); 
}
