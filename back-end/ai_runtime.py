from config import CONFIG


def get_ai_runtime_config(width, height):
    if width == 15 and height == 15:
        return {
            'model_name': '202202281205_15_15_5_1.0_5_400',
            'c_puct': 5,
            'n_playout': 800,
        }
    return {
        'model_name': CONFIG['MODEL_NAME'],
        'c_puct': CONFIG['C_PUCT'],
        'n_playout': CONFIG['N_PLAYOUT'],
    }
