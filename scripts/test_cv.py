"""Regression checks: python -m unittest discover -s scripts -p test_cv.py."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from pypdf import PdfReader
from cv import generate


class CurriculumTests(unittest.TestCase):
    def test_single_page_content_links_and_deterministic_output(self):
        with TemporaryDirectory() as folder:
            first, second = Path(folder) / 'first.pdf', Path(folder) / 'second.pdf'
            generate(first)
            generate(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            pdf = PdfReader(first)
            self.assertEqual(len(pdf.pages), 1)
            page = pdf.pages[0]
            text = page.extract_text()
            for expected in ['José Javier Páez Toledo', 'Dumelis', 'WebSocket', 'SQLite', 'PostgreSQL',
                             'Tanke', 'Iluzona Innova SL', 'Iluzona Control', 'Nett Digital School', 'B2',
                             'Reboot Academy', 'IDIOMAS', 'Inglés']:
                self.assertIn(expected, text)
            for stale in ['DM Command', 'D&D;', 'Supabase', 'Canary Options', 'En curso', '\ufffd']:
                self.assertNotIn(stale, text)
            urls = {annotation.get_object()['/A']['/URI'] for annotation in page['/Annots']}
            self.assertEqual(urls, {
                'https://portfolio.javistudio.dev/', 'https://github.com/JaviPaez7',
                'https://linkedin.com/in/javipaez', 'mailto:javipaeztoledo@gmail.com',
                'https://tanke.javistudio.dev/', 'https://dumelis.javistudio.dev/',
            })


if __name__ == '__main__':
    unittest.main()
