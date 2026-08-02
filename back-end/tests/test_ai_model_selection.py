import unittest

from config import CONFIG
from ai_runtime import get_ai_runtime_config


class TestAiModelSelection(unittest.TestCase):
    def test_15x15_uses_stronger_runtime(self):
        cfg = get_ai_runtime_config(15, 15)
        self.assertEqual(cfg['model_name'], '202202281205_15_15_5_1.0_5_400')
        self.assertGreater(cfg['n_playout'], CONFIG['N_PLAYOUT'])
        self.assertGreaterEqual(cfg['c_puct'], CONFIG['C_PUCT'])

    def test_8x8_keeps_default_runtime(self):
        cfg = get_ai_runtime_config(8, 8)
        self.assertEqual(cfg['model_name'], CONFIG['MODEL_NAME'])
        self.assertEqual(cfg['n_playout'], CONFIG['N_PLAYOUT'])


if __name__ == '__main__':
    unittest.main()
