import os
import shutil

import jinja2

from saliere.core import UsageError


class Templatizer:
    """Template manager.

    Handles all the template related operations.
    """

    def __init__(self, template_path_list=None, template_type=None):
        """Initializer.

        :param template_path_list: the list of paths where the templates are possibly located
        """
        # Use default template paths if none were specified.
        self.template_path_list = template_path_list if template_path_list else ['data/templates',
                                                                                 '../data/templates',
                                                                                 '/usr/local/share/saliere/templates']

        # Set the type if specified.
        self.template_type = template_type

    @staticmethod
    def create_folder(folder, on_failure=None):
        """Creates a folder and the parent directories if needed.

        :param folder: name/path of the folder to create
        :param on_failure: function to execute in case of failure
        """
        try:
            os.makedirs(folder)
        except OSError:
            if on_failure:
                on_failure()

    def copy(self, project_name, output_dir, template_vars=None):
        """Creates the skeleton based on the chosen template.

        :param template_path: the path of the template to use
        :param project_name: the name of the project
        :param output_dir: the path of the output directory
        """
        # Locate the template path.
        template_path = self.locate_template()
        if not template_path:
            raise UsageError("A project type is required.")

        # Ensure the template path ends with a "/".
        template_folder_parent = os.path.abspath(template_path) + "/template/"

        # Prepare the output directory.
        output_folder_root = os.path.abspath(output_dir)

        # List of the files in the template folder.
        for root, subfolders, files in os.walk(template_path):

            # Prepare the jinja environment.
            template_loader = jinja2.FileSystemLoader(root)
            jinja_env = jinja2.Environment(loader=template_loader)

            # Recreate the folders with the formula name
            skeleton_folder_path = os.path.join(output_folder_root, project_name)
            current_skeleton_folder_path = (root + '/').replace(template_folder_parent, '')
            dst_folder = os.path.join(skeleton_folder_path, current_skeleton_folder_path)
            Templatizer.create_folder(dst_folder)

            # List the files.
            for file in files:
                dst = os.path.join(skeleton_folder_path, file) if current_skeleton_folder_path == '' else os.path.join(
                    skeleton_folder_path, current_skeleton_folder_path, file)

                # If there is no variables to replace, simply copy the file.
                if not template_vars:
                    src = os.path.join(root, file)
                    shutil.copyfile(src, dst)
                    continue

                # Otherwise jinjanize it.
                jinjanized_content = Jinjanizer.jinjanize(jinja_env, file, template_vars)

                # Create the file with the rendered content.
                with open(dst, mode='w', encoding='utf-8') as jinjanized_file:
                    jinjanized_file.write(jinjanized_content)

    def list_templates(self):
        """Returns a list of available templates ordered alphabetically.

        :return: a list of available templates ordered alphabetically
        """
        # Ensure we have a list of paths.
        if not self.template_path_list:
            return None

        # Initialize an empty set of available templates.
        available_templates = set()

        # Go through the list of valid paths.
        for path in self.template_path_list:
            base_path = os.path.abspath(path)
            try:
                subdirs = os.listdir(base_path)
                available_templates.update(subdirs)
            except FileNotFoundError:
                pass

        # Return a list of available templates ordered alphabetically.
        return sorted(available_templates)

    def locate_template(self, template_type=None):
        """Returns the path of a template.

        Given a template type the function will attempt to retrieve its full path. If instead of a template type, a
        full path is given, the function will validate the full path, If the full path cannot be determined, the
        function returns None.

        :param template_type: the type of the template or its full path
        :return: the path of the template or None if it does not exist
        """
        # Ensure we have a template type.
        if not template_type:
            template_type = self.template_type
        if not template_type:
            return None

        # If the template type is a valid custom path, return it.
        if os.path.exists(template_type):
            return template_type

        # Ensure we have a list of paths.
        if not self.template_path_list:
            return None

        # Go through the list of valid paths.
        for path in self.template_path_list:
            base_path = os.path.abspath(path)
            template_path = os.path.join(base_path, template_type)
            is_valid = os.path.exists(template_path)
            if is_valid:
                break

        # Return the full path of the given template or None if it cannot be found.
        return os.path.abspath(template_path) if is_valid else None


class Jinjanizer:
    """Handle the jinjanization of the templates.

    """

    @staticmethod
    def jinjanize(jinja_env, template_file, template_vars=None):
        """Renders a Jinja2 template.

        :param jinja_env: the jinja environment
        :param template_file: the full path of the template file to render
        :param formula_name: the name of the formula
        :return: a string representing the rendered template
        """
        if not template_vars:
            template_vars = {}

        # Load the template
        template = jinja_env.get_template(template_file)

        # Render the template and return the result
        return template.render(template_vars)
