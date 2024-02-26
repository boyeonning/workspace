import ast
import time

from loguru import logger
from flask import Flask, request
from error_code.error_code import *

from logic.main import AutoFeature


class MakeFeature:
    def __init__(self, revision):
        self.app = Flask(__name__)
        self.revision = revision
        self.make_feature = AutoFeature()

    def api(self):
        try:
            user_id = request.headers['USER-ID']
        except Exception as e:
            logger.warning(f'Request does not set the Userid, {e}')
            user_id = 'unknown'
        logger.info(f'Processing user request from user id [{user_id}], revision {self.revision}')

        start = time.time()

        if request.method == 'POST':
            result = {}
            try:
                payload = ast.literal_eval(request.get_data().decode("UTF-8"))
                images = payload.get('images')
                pog_name = payload.get('pog_name')
                version = payload.get('version', '0')
                logger.info(f'🍓[pog_name=[{pog_name}], version={version}]🥭')

            except Exception as e:
                err = InputError(msg=e)
                result['status'] = err.code
                result['message'] = err.message
                logger.exception(result['message'])
                return result

            err = None
            try:
                result['res'] = self.make_feature.run(images, pog_name, version)
                end = time.time()
                logger.success(
                    f'Make Feature API success for request from {user_id} | [process time]: {round(end - start, 2)} \n')
            except Exception as e:
                err = e
                logger.exception(f'🔴 Make Feature failed due to {err.message}')
            finally:
                result['status'] = Good.code if err is None else err.code
                result['message'] = Good.message if err is None else err.message

            return result
