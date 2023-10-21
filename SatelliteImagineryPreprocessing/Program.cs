// See https://aka.ms/new-console-template for more information

using System.Buffers;
using System.Diagnostics;
using TiffLibrary;
using TiffLibrary.PixelFormats;


var workingDirectory = Environment.CurrentDirectory;
var projectDirectory = Directory.GetParent(workingDirectory).Parent.Parent.FullName;

var sw = new Stopwatch();
sw.Start();


await using var tiff = await TiffFileReader.OpenAsync(projectDirectory+ @"\Examples\large_file.tif");

using var fieldReader = await tiff.CreateFieldReaderAsync();
var ifd = await tiff.ReadImageFileDirectoryAsync();
var tagReader = new TiffTagReader(fieldReader, ifd);

// Get offsets to the strip/tile data
TiffValueCollection<ulong> offsets, byteCounts;
if (ifd.Contains(TiffTag.TileOffsets))
{
    offsets = await tagReader.ReadTileOffsetsAsync();
    byteCounts = await tagReader.ReadTileByteCountsAsync();
}
else if (ifd.Contains(TiffTag.StripOffsets))
{
    offsets = await tagReader.ReadStripOffsetsAsync();
    byteCounts = await tagReader.ReadStripByteCountsAsync();
}
else
{
    throw new InvalidDataException("This TIFF file is neither striped or tiled.");
}
if (offsets.Count != byteCounts.Count)
{
    throw new InvalidDataException();
}

// Extract strip/tile data
using var contentReader = await tiff.CreateContentReaderAsync();
int count = offsets.Count;
for (int i = 0; i < count; i++)
{
    var offset = (long)offsets[i];
    var byteCount = (int)byteCounts[i];
    var data = ArrayPool<byte>.Shared.Rent(byteCount);
    try
    {
        await contentReader.ReadAsync(offset, data.AsMemory(0, byteCount));
        await using var fs = new FileStream(  projectDirectory+ $@"\Results\extracted-{i}.dat", FileMode.Create, FileAccess.Write);
        await fs.WriteAsync(data, 0, byteCount);
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(data);
    }
}

sw.Stop();


Console.WriteLine("Elapsed={0}",sw.Elapsed);





