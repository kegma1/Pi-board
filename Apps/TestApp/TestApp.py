from libs.App import App

class TestApp(App):
    def get_image(self):
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>Pi-board Display</title>
            <style>
                html, body {
                margin: 0;
                padding: 0;
                width: 800px;
                height: 480px;
                overflow: hidden;
                font-family: sans-serif;
                background-color: #f0f0f0;
                }

                #app-container {
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                }

                h1 {
                font-size: 36px;
                margin: 0;
                }

                p {
                font-size: 20px;
                margin-top: 10px;
                }
            </style>
            </head>
            <body>
            <div id="app-container">
                <h1>Hello, Pi-board!</h1>
                <p>This fits exactly 800×480 pixels.</p>
            </div>
            </body>
            </html>
        
        '''