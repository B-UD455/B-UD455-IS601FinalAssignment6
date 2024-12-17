'''
import markdown2
from pathlib import Path

class TemplateManager:
    def __init__(self):
        # Dynamically determine the root path of the project
        self.root_dir = Path(__file__).resolve().parent.parent.parent  # Adjust this depending on the structure
        self.templates_dir = self.root_dir / 'email_templates'

    def _read_template(self, filename: str) -> str:
        """Private method to read template content."""
        template_path = self.templates_dir / filename
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _apply_email_styles(self, html: str) -> str:
        """Apply advanced CSS styles inline for email compatibility with excellent typography."""
        styles = {
            'body': 'font-family: Arial, sans-serif; font-size: 16px; color: #333333; background-color: #ffffff; line-height: 1.5;',
            'h1': 'font-size: 24px; color: #333333; font-weight: bold; margin-top: 20px; margin-bottom: 10px;',
            'p': 'font-size: 16px; color: #666666; margin: 10px 0; line-height: 1.6;',
            'a': 'color: #0056b3; text-decoration: none; font-weight: bold;',
            'footer': 'font-size: 12px; color: #777777; padding: 20px 0;',
            'ul': 'list-style-type: none; padding: 0;',
            'li': 'margin-bottom: 10px;'
        }
        # Wrap entire HTML content in <div> with body style
        styled_html = f'<div style="{styles["body"]}">{html}</div>'
        # Apply styles to each HTML element
        for tag, style in styles.items():
            if tag != 'body':  # Skip the body style since it's already applied to the <div>
                styled_html = styled_html.replace(f'<{tag}>', f'<{tag} style="{style}">')
        return styled_html

    def render_template(self, template_name: str, **context) -> str:
        """Render a markdown template with given context, applying advanced email styles."""
        header = self._read_template('header.md')
        footer = self._read_template('footer.md')

        # Read main template and format it with provided context
        main_template = self._read_template(f'{template_name}.md')
        main_content = main_template.format(**context)

        full_markdown = f"{header}\n{main_content}\n{footer}"
        html_content = markdown2.markdown(full_markdown)
        return self._apply_email_styles(html_content)
    '''

import markdown2
from pathlib import Path
import os

class TemplateManager:
    def __init__(self):
        # Dynamically determine the root path of the project
        self.root_dir = Path(__file__).resolve().parent.parent.parent  # Adjust this depending on the structure
        self.templates_dir = self.root_dir / 'email_templates'

        # Ensure the templates directory exists
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"The templates directory {self.templates_dir} does not exist.")

    def _read_template(self, filename: str) -> str:
        """Private method to read template content."""
        template_path = self.templates_dir / filename
        if not template_path.exists():
            raise FileNotFoundError(f"Template file {filename} not found in {self.templates_dir}.")
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _apply_email_styles(self, html: str) -> str:
        """Apply advanced CSS styles inline for email compatibility with excellent typography."""
        # Define styles as a single CSS block to minimize repetitive inline styles
        css = """
            body { font-family: Arial, sans-serif; font-size: 16px; color: #333333; background-color: #ffffff; line-height: 1.5; }
            h1 { font-size: 24px; color: #333333; font-weight: bold; margin-top: 20px; margin-bottom: 10px; }
            p { font-size: 16px; color: #666666; margin: 10px 0; line-height: 1.6; }
            a { color: #0056b3; text-decoration: none; font-weight: bold; }
            footer { font-size: 12px; color: #777777; padding: 20px 0; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
        """
        # Wrap HTML content with a <style> tag and inline styles
        styled_html = f'<style>{css}</style><div>{html}</div>'
        return styled_html

    def render_template(self, template_name: str, **context) -> str:
        """Render a markdown template with given context, applying advanced email styles."""
        try:
            # Read header, footer, and main template
            header = self._read_template('header.md')
            footer = self._read_template('footer.md')

            # Read main template and format it with provided context
            main_template = self._read_template(f'{template_name}.md')
            main_content = main_template.format(**context)

            # Combine all parts
            full_markdown = f"{header}\n{main_content}\n{footer}"

            # Convert markdown to HTML
            html_content = markdown2.markdown(full_markdown)

            # Apply email styles and return the result
            return self._apply_email_styles(html_content)

        except FileNotFoundError as e:
            raise ValueError(f"Template rendering failed: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred while rendering the template: {e}")

