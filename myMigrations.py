# IMPORTS
from mstrio.connection import Connection
from mstrio.object_management import (
    Folder
)
from mstrio.object_management.migration import (
    Migration,
    PackageConfig,
    PackageContentInfo,
    PackageSettings
)
from mstrio.types import ObjectTypes

from Constants import *


# ******************************************************************** FUNCTIONS *********************************************

def f_package_content_info(objetos_migrar: ObjectTypes) -> object:
    # funcion que crea  el contenido de la migracion introduciendo la info una lista.
    # usa la funcion PackageContentInfo
    # se lel indica el tipo de objeto asi como la acion a realizar con ese objeto  y se se quiere llevar dependencias.

    objetos = []

    for i in objetos_migrar:  # Recorremos  la lista de objetos
        if len(i) > 0:
            package_content_info = PackageContentInfo(
                id=i[0]["id"],
                type=i[0]["type"],
                action=PackageContentInfo.Action.FORCE_REPLACE,
                include_dependents=True,
            )
        objetos.append(package_content_info)

    return objetos


def mstr_create_conection(base_url, username, password, project_name) -> object:
    # Connect to the MicroStrategy server
    source_conn = Connection(base_url, username, password, project_name=project_name, login_mode=1)
    return source_conn


def MigrarObjetos(package_content_info, source_conn, target_conn, save_path):
    # Create PackageConfig with information what object should be migrated and how.
    # The options are of type Enum with all possible values listed.

    package_settings = PackageSettings(
        PackageSettings.DefaultAction.USE_EXISTING,
        PackageSettings.UpdateSchema.RECAL_TABLE_LOGICAL_SIZE,
        PackageSettings.AclOnReplacingObjects.REPLACE,
        PackageSettings.AclOnNewObjects.KEEP_ACL_AS_SOURCE_OBJECT,
    )

    package_config = PackageConfig(
        PackageConfig.PackageUpdateType.PROJECT, package_settings, package_content_info
    )

    # Create Migrations objects that can use all the functionalities
    mig = Migration(
        save_path=save_path,
        source_connection=source_conn,
        target_connection=target_conn,
        configuration=package_config,
    )
    try:
        # mig.perform_full_migration()
        mig.create_package()
        mig.migrate_package()
        print(mig.status)
    except:
        print("An exception occurred")
        # print(mig.status)
        raise


def create_package(base_url, username, password, folder_id, package_name, package_description, project_name):
    # Connect to the MicroStrategy server
    # Create connections to both source and target environments

    # conexiones
    # obtener objetos primarios
    # perform migration

    source_conn = Connection(
        SOURCE_BASE_URL, SOURCE_USERNAME, SOURCE_PASSWORD, project_name=PROJECT_NAME, login_mode=1
    )
    target_conn = Connection(
        TARGET_BASE_URL, TARGET_USERNAME, TARGET_PASSWORD, project_name=PROJECT_NAME_TARGET, login_mode=1
    )

    # obtenemos la carpeta migracion
    folder = Folder(source_conn, id=folder_id)
    print("Buscando objetos en la carpeta --> ", folder.name)
    contents_objs = folder.get_contents()  # obtenemos el contenido de la carpeta

    # declaramos la lista para el contenido a migrar
    SobjectToMigrate = []

    for sObject in contents_objs:
        if sObject.type == ObjectTypes.SHORTCUT_TYPE:  # Solo queremos los accesos directos
            # Añadimos a la lista SobjectToMigrate las dependencias del acceso directo que es el objeto a migrar
            # aqui la duda. Que tipos. Para DATIO, solo Cubos, Documentos, Dossieres, Atributos, Informes, Custom Groups.....
            SobjectToMigrate.append(sObject.list_dependencies())
            # SobjectToMigrate.append(sObject.list_dependencies(object_types=ObjectTypes.REPORT_DEFINITION))
            # SobjectToMigrate.append(sObject.list_dependencies(object_types=ObjectTypes.DOCUMENT_DEFINITION)) # Dossieres de un accso
            # SobjectToMigrate.append(sObject.list_dependencies(object_types=ObjectSubTypes.SUPER_CUBE)) #revissar

    # SobjectToMigrate=list(filter(None, SobjectToMigrate)) #elimiar vacios
    # Buscamos las dependencias para añadir unicamente como user existeste.

    SobjectToMigrate = list(filter(None, SobjectToMigrate))  # elimiar vacios
    SobjectToMigrate.reverse()

    #    SobjectToMigrate = list(dict.fromkeys(SobjectToMigrate)) #eliminar duplciados

    package_content_info = []
    if len(SobjectToMigrate) == 0:
        print("No hay shortcuts en la carpeta de migraciones")
    else:
        package_content_info = f_package_content_info(SobjectToMigrate)
        MigrarObjetos(package_content_info, source_conn, target_conn, package_name)

#    print("Package created successfully with name: {} and id: {}".format(package_name, package_id))
