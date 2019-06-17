from quizzes.tests.test_embed import embed_test_quizzes
from core.tests.test_embed import embed_test_locations

def test_locations():
    print('embeding...')
    embed_test_locations()
    print('done')
    
def test_quizzes():    
    print('embeding...')
    embed_test_quizzes()
    print('done')