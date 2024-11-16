class GradioComponentsHTML:

    @staticmethod
    def get_html_header() -> str:
        return """
        <div style="text-align: center; max-width: 1100px; margin: 0 auto;">
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 10px;
                padding: 20px;
                border-radius: 10px;
                background: linear-gradient(to right, #2d2d2d, #1a1a1a);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            ">
                <div style="display: flex; flex-direction: column; align-items: flex-start;">
                    <h1 style="
                        font-size: 2.5rem;
                        font-weight: 600;
                        margin: 0;
                        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">
                        ShortFactory
                    </h1>
                    <p style="
                        margin: 5px 0 0 0;
                        color: #888;
                        font-size: 1.1rem;
                    ">
                        Create Engaging Social Media Videos with AI
                    </p>
                </div>
            </div>
        </div>
        """

    @staticmethod
    def get_html_footer() -> str:
        return """
        <div style="
            text-align: center;
            padding: 20px;
            margin-top: 50px;
            border-top: 1px solid #444;
        ">
            <p style="color: #888; margin: 0;">
                Made with ❤️ by ShortFactory
            </p>
        </div>
        """

    @staticmethod
    def get_html_video_template(file_url_path, file_name, width="auto", height="auto"):
        """
        Generate an HTML code snippet for embedding and downloading a video.

        Parameters:
        file_url_path (str): The URL or path to the video file.
        file_name (str): The name of the video file.
        width (str, optional): The width of the video. Defaults to "auto".
        height (str, optional): The height of the video. Defaults to "auto".

        Returns:
        str: The generated HTML code snippet.
        """
        html = f'''
            <div style="display: flex; flex-direction: column; align-items: center;">
                <video width="{width}" height="{height}" style="max-height: 100%;" controls>
                    <source src="{file_url_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                </a>
            </div>
        '''
        return html

    @staticmethod
    def get_html_video_preview(video_path):
        return f"""
        <div style="
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        ">
            <video
                width="100%"
                height="auto"
                controls
                style="display: block;"
            >
                <source src="{video_path}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        """

    @staticmethod
    def get_html_template_card(template_name, description, features):
        features_html = "".join([f"<li>{feature}</li>" for feature in features])
        return f"""
        <div style="
            background: #2d2d2d;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        ">
            <h3 style="
                margin: 0 0 10px 0;
                color: #fff;
                font-size: 1.2rem;
            ">{template_name}</h3>
            <p style="
                color: #888;
                margin: 0 0 15px 0;
                font-size: 0.9rem;
            ">{description}</p>
            <ul style="
                color: #888;
                margin: 0;
                padding-left: 20px;
                font-size: 0.9rem;
            ">{features_html}</ul>
        </div>
        """

    @staticmethod
    def get_html_status(message, status_type="info"):
        colors = {
            "info": "#3498db",
            "success": "#2ecc71",
            "warning": "#f1c40f",
            "error": "#e74c3c"
        }
        return f"""
        <div style="
            background: {colors[status_type]}22;
            border-left: 4px solid {colors[status_type]};
            color: {colors[status_type]};
            padding: 10px 15px;
            margin: 10px 0;
            border-radius: 4px;
            font-size: 0.9rem;
        ">
            {message}
        </div>
        """

    @staticmethod
    def get_html_error_template() -> str:
        return '''
        <div style='text-align: center; background: #f2dede; color: #a94442; padding: 20px; border-radius: 5px; margin: 10px;'>
          <h2 style='margin: 0;'>ERROR : {error_message}</h2>
          <p style='margin: 10px 0;'>Traceback Info : {stack_trace}</p>
          <p style='margin: 10px 0;'>If the problem persists, don't hesitate to contact our support. We're here to assist you.</p>
          <a href='https://discord.gg/qn2WJaRH' target='_blank' style='background: #a94442; color: #fff; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none;'>Get Help on Discord</a>
        </div>
        '''
