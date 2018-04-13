import subprocess
import os
#filename without filetype
M_HOME = "/home/fenics/acc11"
FENICS_PATH = "home/fenics/shared/"
SYNC_RESULTS_PATH = M_HOME + "/sync_results/"
AIRFOIL_PATH = M_HOME + "/murtazo/navier_stokes_solver/"
MESH_FILE_PATH = M_HOME + "/murtazo/cloudnaca/msh/"
MESH_SHELL_PATH = M_HOME +"/murtazo/cloudnaca/"
TAR_RESULTS_PATH = M_HOME + "/murtazo/navier_stokes_solver/"
RESULTS_PATH = TAR_RESULTS_PATH + "results/"
MASTER_ADDRESS = "ubuntu@localhost"
MASTER_SYNC_RESULTS_PATH = "/home/ubuntu/sync_results"
MASTER_RSYNC_ADDRESS = MASTER_ADDRESS + ":" + MASTER_SYNC_RESULTS_PATH
RSYNC_SSH = 'ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no'
GEO_FILE_PATH = M_HOME + "/murtazo/cloudnaca/msh/"

def make_mesh(min_angle,max_angle,n_angles,points,refinements,naca):
        os.chdir(MESH_SHELL_PATH)
        naca_1 = naca[0]
        naca_2 = naca[1]
        naca_3 = naca[2]
        naca_4 = naca[3]
        runme_path = MESH_SHELL_PATH + "runme.sh"
        print runme_path
        #subprocess.call(["ls", "/home/fenics/shared"])
        subprocess.call(['bash',runme_path,  str(min_angle), str(max_angle),str(n_angles),str(points),str(refinements),str(naca_1),str(naca_2),str(naca_3),str(naca_4)])
        #shell=True as 2nd arg

def make_mesh_to_xml(filename):
        os.chdir(MESH_FILE_PATH)
        filename_path = MESH_FILE_PATH + filename
        subprocess.call(["dolfin-convert",filename_path + '.msh',filename_path + '.xml'])
def make_airfoil(samples, viscosity, velocity,sim_time,filename):
        os.chdir(AIRFOIL_PATH)
        filename_path = MESH_FILE_PATH + filename + ".xml"
        print filename_path
        #subprocess.call(["ls",AIRFOIL_PATH])
        #subprocess.call(["ls",MESH_FILE_PATH])
        subprocess.call(["./airfoil",str(samples), str(viscosity),str(velocity),str(sim_time),filename_path])

def add_meshes_and_geo_to_results(mesh_filename,geo_filename):
        os.chdir(GEO_FILE_PATH)
        subprocess.call(['cp',geo_filename + ".geo",RESULTS_PATH])
        os.chdir(MESH_FILE_PATH)
        subprocess.call(['cp',mesh_filename + ".xml",RESULTS_PATH])
        subprocess.call(['cp',mesh_filename + ".msh",RESULTS_PATH])

def remove_meshes_and_geo_from_results(mesh_filename,geo_filename):
        os.chdir(RESULTS_PATH)
        subprocess.call(['rm',geo_filename + ".geo"])
        subprocess.call(['rm',mesh_filename + ".xml"])
        subprocess.call(['rm',mesh_filename + ".msh"])

def compress_results(result_filename):
        os.chdir(SYNC_RESULTS_PATH)
        #subprocess.call(["ls",RESULTS_PATH])
        #subprocess.call(["ls",FENICS_PATH])
        subprocess.call(["tar", "-zcvf", SYNC_RESULTS_PATH + result_filename + ".tar.gz", "-C", TAR_RESULTS_PATH, "results/"])

def sync_results_with_master():
        os.chdir(SYNC_RESULTS_PATH)
        subprocess.call(["rsync", "-chavze", "{}".format(RSYNC_SSH), SYNC_RESULTS_PATH, MASTER_RSYNC_ADDRESS])

def do_single_mesh_result(angle,points,refinements, naca,samples,viscosity,velocity,sim_time,result_filename):
        make_mesh(angle,angle,1,points,refinements,naca)
        angle_str =  "a" + str(angle)
        #.replace(".","_")
        points_str =  "n" + str(points)
        #.replace(".","_")
        refinements_str =  "r"  + str(refinements)
        #.replace(".","_")
        mesh_filename = refinements_str + angle_str + points_str
        geo_filename = refinements_str + angle_str + points_str

        make_mesh_to_xml(mesh_filename)
        make_airfoil(samples,viscosity,velocity,sim_time,mesh_filename)
        add_meshes_and_geo_to_results(mesh_filename,geo_filename)
        compress_results(result_filename)
        remove_meshes_and_geo_from_results(mesh_filename,geo_filename)
        sync_results_with_master()
        return result_filename + '.tar.gz'

def test_all():
        do_single_mesh_result(20,200,0,"0012",1,0.0001,10.0,0.01,"TEST_TAR")

if __name__ == "__main__":
        test_all()
