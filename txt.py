import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
import django
django.setup()

def main():
    from article.models import Article
    f = open('txt.txt', encoding="UTF-8")
    ArticleList = [Article(title=line.split("**")[0],
                           content=line.split("**")[1],
                           created=line.split("**")[2],
                           update=line.split("**")[3],
                           total_views=line.split("**")[4],
                           author_id=line.split("**")[5],
                           column_id=line.split("**")[6],
                           likes=line.split("**")[7]) for line in f]
    # for line in f:
    #     parts = line.split('**')
    #     # ArticleList.append(Article(title=parts[0], content=parts[1]))

    Article.objects.bulk_create(ArticleList)

    f.close()
if __name__ == "__main__":
    main()
    print('Done!')