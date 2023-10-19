// See https://aka.ms/new-console-template for more information

using TiffLibrary;


var workingDirectory = Environment.CurrentDirectory;
var projectDirectory = Directory.GetParent(workingDirectory).Parent.Parent.FullName;

await using TiffFileReader tiff = await TiffFileReader.OpenAsync(projectDirectory+ @"\Examples\NmTHIR115-1T.N6.asc.1975.313.21.09.16.1929.2020.159.tif");


Console.WriteLine("Hello, World!");