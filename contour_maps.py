import vtk
import sys

def main(options):
    vtk_file = options[0]
    #read vtk
    vtk_reader = read_vtk(vtk_file)
    #Render image
    render_image(vtk_reader)

def read_vtk(vtk_file):
    vtk_reader = vtk.vtkStructuredPointsReader()
    vtk_reader.SetFileName(vtk_file)
    vtk_reader.Update() 
    return vtk_reader

def render_image(vtk_reader):
    contour = vtk.vtkContourFilter()
    contour.SetInput(vtk_reader.GetOutput())
    contour.GenerateValues(20,20,200)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(contour.GetOutput())
    mapper.ScalarVisibilityOn()
    mapper.SetScalarRange(0,255)

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
    main(sys.argv[1:])
