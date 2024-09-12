class User:
    """
    Класс пользователя, содержащий атрибуты:
                        nickname(имя пользователя, строка),
                        password(в хэшированном виде, число),
                        age(возраст, число))
    """
    def __new__(cls, *args):
        return object.__new__(cls)

    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age


class Video:
    """
    Класс видио, содержащий атрибуты:
                        title(заголовок, строка),
                        duration(продолжительность, секунды),
                        time_now(секунда остановки (изначально 0)),
                        adult_mode(ограничение по возрасту,
                        bool (False по умолчанию)
    """
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class UrTube:
    """
    Класс платформы университета Urban, содержащий:
            Атриубты:   users(список объектов User),
                        videos(список объектов Video),
                        current_user(текущий пользователь)
            Методы:
                        log_in, который принимает на вход аргументы:
                            nickname, password (пытается найти пользователя в users с такими же логином и паролем.
                            Eсли такой пользователь существует, меняет current_user на найденного).

                        register, который принимает три аргумента:
                            nickname, password, age (добавляет пользователя в список, если пользователя не существует
                            с таким же nickname.
                            Если существует, выводит на экран: "Пользователь уже существует".
                            После регистрации, вход выполняется автоматически.

                        log_out для сброса текущего пользователя на None.

                        add, который принимает неограниченное кол-во объектов класса Video и все добавляет в videos,
                            если с таким же названием видео ещё не существует.В противном случае ничего не происходит.

                        get_videos, который принимает поисковое слово и возвращает список названий всех видео,
                            содержащих поисковое слово.

                        watch_video, который принимает название фильма, если не находит точного совпадения,
                            то ничего не воспроизводится, если же находит - ведётся отчёт в консоль на какой секунде
                            ведётся просмотр. После текущее время просмотра данного видео сбрасывается.
    """
    videos = {}
    users = {}
    current_user = None

    @staticmethod
    def register(nickname, password, age):
        if nickname in UrTube.users:
            print(f'Пользователь {nickname} уже существует')
        else:
            hash_password = hash(password)
            UrTube.users[nickname] = [hash_password, age]
            User(nickname, hash_password, age)
            UrTube.current_user = nickname

    @staticmethod
    def log_in(nickname, password):
        if nickname in UrTube.users and hash(password) in UrTube.users[nickname]:
            UrTube.current_user = nickname

    @staticmethod
    def log_out():
        UrTube.current_user = None

    @staticmethod
    def add(*args):
        for i in range(len(args)):
            if args[i].title not in UrTube.videos:
                UrTube.videos[args[i].title] = [args[i].duration, args[i].time_now, args[i].adult_mode]
        print(list(UrTube.videos.keys()))

    @staticmethod
    def get_videos(key_word):
        list_video = []
        list_keys = list(UrTube.videos.keys())
        for i in range(len(list_keys)):
            if key_word.lower() in list_keys[i].lower():
                list_video.append(list_keys[i])
        return list_video

    @staticmethod
    def watch_video(title):
        from time import sleep
        if title in UrTube.videos:
            if UrTube.current_user is None:
                print('Войдите в аккаунт, чтобы смотреть видео')
            elif UrTube.videos[title][2] and UrTube.users[UrTube.current_user][1] < 18:
                print('Вам нет 18 лет, пожалуйста покиньте страницу')
            else:
                for i in range(UrTube.videos[title][1], UrTube.videos[title][0]):
                    sleep(1)
                    print(i+1, end=" ")
                print('Конец видео')


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
