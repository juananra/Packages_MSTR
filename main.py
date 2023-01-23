from Constants import *
from Utilidades import *
from myMigrations import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    package_name = format_package_name(PROJECT_NAME)
    package_name_and_path = SAVE_PATH + '\\' + package_name
    print(package_name_and_path)

    create_package(SOURCE_BASE_URL, SOURCE_USERNAME, SOURCE_PASSWORD, FOLDER_ID, package_name_and_path,
                   PACKAGE_DESCRIPTION, PROJECT_NAME)
