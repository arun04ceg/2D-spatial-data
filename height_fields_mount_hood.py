import vtk
import sys

def main(options):
    png_file = options[0]
    #Read png
    png_reader = read_png(png_file)
    #render image
    render_image(png_reader)

def read_png(png_file):
    png_reader = vtk.vtkPNMReader()
    png_reader.SetFileName(png_file)
    return png_reader

def render_image(png_reader):
    colorLookup = vtk.vtkLookupTable()
    colorLookup.SetNumberOfColors(256)
    colorLookup.SetTableRange(0, 255)
    for ii in range(0, 256):
        colorLookup.SetTableValue(ii, 0, 0, 0, 1)

    magnitude = vtk.vtkImageMagnitude()
    magnitude.SetInput(png_reader.GetOutput())

    geometry = vtk.vtkImageDataGeometryFilter()
    geometry.SetInput(magnitude.GetOutput())

    warp = vtk.vtkWarpScalar()
    warp.SetInput(geometry.GetOutput())
    warp.SetScaleFactor(0.25)

    merge = vtk.vtkMergeFilter()
    merge.SetGeometry(warp.GetOutput())
    merge.SetGeometry(warp.GetOutput())
    merge.SetScalars(png_reader.GetOutput())

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInput(merge.GetOutput())
    mapper.ScalarVisibilityOn()
    mapper.SetLookupTable(colorLookup)
    #mapper.SetScalarRange(0,255)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(.5, .5, .5)

    renderWindow.SetSize(600, 600)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == "__main__":
    options = sys.argv[1:]
    main(options)
