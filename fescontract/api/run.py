from flask import Flask, jsonify
import pandas as pd
from get_participants import download_scorecards
from flask_cors import CORS

app = Flask(__name__, static_folder='../', static_url_path='/')
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_data')
def get_scorecards():
    app.logger.info(f'Read file with scorecards')
    df = pd.read_excel('participants.xls')
    df = df[df['LT DATE'].notna()]
    df = df[['NAME', 'EMAIL', 'STARTDATE', 'LT DATE',
             'LT SCORE', 'LT SCORE POINTS', 'LUT DATE',
             'LUT SCORE', 'LUT SCORE POINTS']]
    df['points'] = df.apply(lambda x: x['LUT SCORE POINTS'] if x['LUT SCORE POINTS'] > 0 else x['LT SCORE POINTS'],
                            axis=1)
    df = df.fillna(False)
    df['level'] = df.apply(
        lambda x: x['LUT SCORE'] if x['LUT SCORE'] else x['LT SCORE'],
        axis=1)
    df['date'] = df.apply(
        lambda x: x['LUT DATE'] if x['LUT DATE'] else x['LT DATE'],
        axis=1)

    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['testType'] = df.apply(
        lambda x: 'LUT' if x['LUT SCORE POINTS'] > 0 else 'LT',
        axis=1)
    df.reset_index(inplace=True)
    df.rename(columns={'NAME': 'name',
                       'EMAIL': 'email',
                       'STARTDATE': 'startdate',
                       'index': 'key'},
              inplace=True)
    app.logger.info('File was read and handled')
    return df[['key', 'name', 'email', 'points',
               'level', 'testType', 'date']].to_json(orient='records',
                                                     date_format='iso')


@app.route('/update')
def update_scorecards():
    is_downloaded = download_scorecards(logger=app.logger)
    return {'status': 'SUCCESS' if is_downloaded else 'FAILED'}


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
