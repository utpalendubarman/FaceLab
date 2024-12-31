import os
import shutil

def CleanDirectories(project_id):
    try:
        sources=os.listdir(f"projects/{project_id}/source")
        targets=os.listdir(f"projects/{project_id}/target")

        obj={
            "source":sources,
            "target":targets
        }

        for source in sources:
            if source=='__MACOSX':
                shutil.rmtree(f"projects/{project_id}/source/__MACOSX")
            else:
                allFiles=os.listdir(f"projects/{project_id}/source/{source}")
                for file in allFiles:
                    shutil.move(f"projects/{project_id}/source/{source}/{file}",f"projects/{project_id}/source")
                shutil.rmtree(f"projects/{project_id}/source/{source}")

        for target in targets:
            if target=='__MACOSX':
                shutil.rmtree(f"projects/{project_id}/target/__MACOSX")
            else:
                allFiles=os.listdir(f"projects/{project_id}/target/{target}")
                for file in allFiles:
                    shutil.move(f"projects/{project_id}/target/{target}/{file}",f"projects/{project_id}/target")
                shutil.rmtree(f"projects/{project_id}/target/{target}")


        return obj
    except Exception as e:
        return {'error':e}
    return False

