import vtk
import sys
import re

def main(options):
    data_file, pts_file, vtk_file = options
    #parse_data_file
    z_list = parse_data_file(data_file)
    #parse_pts_file
    xy_list = parse_pts_file(pts_file)
    #Construct polydata
    pointset = construct_and_write_poly_data(xy_list, z_list, vtk_file)
    #Render Image
    render_image(pointset)

def parse_data_file(data_file):
    z_list = []
    in_file = open(data_file)
    for line in in_file:
        line = line.strip()
        z_list.append(float(line))
    in_file.close()
    return z_list

def parse_pts_file(pts_file):
    xy_list = []
    in_file = open(pts_file)
    for line in in_file:
        line = cleanup_line(line)
        x, y, dummy = line.split(" ")
        xy_list.append((float(x), float(y)))
    in_file.close()
    return xy_list

def construct_and_write_poly_data(xy_list, z_list, vtk_file):
    points = vtk.vtkPoints()
    for ii, xy in enumerate(xy_list):
        points.InsertPoint(ii, xy[0], xy[1], z_list[ii])
    pointset = vtk.vtkPolyData()
    pointset.SetPoints(points)
    writer = vtk.vtkPolyDataWriter()
    writer.SetInput(pointset)
    writer.SetFileName(vtk_file)
    writer.Write()
    return pointset

def render_image(pointset):
    '''
    square = 10
    color_map = vtk.vtkLookupTable()
    color_map.SetNumberOfColors(square * square)
    color_map.SetTableRange(0, square * square - 1)
    for ii in range(0, square):
        for jj in range(0, square):
            color_map.SetTableValue(ii, jj / square, jj / square, ii /square)
    '''

    color_map = vtk.vtkLookupTable()
    color_map.SetNumberOfColors(16)
    color_map.SetHueRange(0, 0.667)

    delaunay = vtk.vtkDelaunay2D()
    delaunay.SetTolerance(0.001)
    delaunay.SetAlpha(18)
    delaunay.SetInput(pointset);
    delaunay.Update();

    elevation_thorax = vtk.vtkElevationFilter()
    elevation_thorax.SetInput(delaunay.GetOutput())
    elevation_thorax.SetLowPoint(0, 0, -25)
    elevation_thorax.SetHighPoint(0, 0, 25)

 
    meshMapper = vtk.vtkPolyDataMapper2D()
    meshMapper.SetInput(elevation_thorax.GetOutput())
    meshMapper.SetLookupTable(color_map)
    #meshMapper.SetScalarRange(0,255)
 
    meshActor = vtk.vtkActor2D()
    meshActor.SetMapper(meshMapper)

    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderer.AddActor(meshActor)
    #renderer.AddActor(boundaryActor)
    renderer.SetBackground(.5, .5, .5)

    renderWindow.SetSize(600, 600) 
    renderWindow.Render()
    renderWindowInteractor.Start()

def cleanup_line(line):
    line = line.strip()
    line = re.sub("\s+", " ", line)
    return line

if __name__ == "__main__":
    options = sys.argv[1:]
    main(options)
