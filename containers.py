from dependency_injector import containers, providers
from note.application.note_service import NoteService
from note.infra.repository.note_repo import NoteRepository
from user.application.email_service import EmailService
from user.application.user_service import UserService

from user.infra.repository.user_repo import UserRepository


class Container(containers.DeclarativeContainer):
    """
    의존성을 사용할 모듈을 선언함. 만약 특정 모듈에만 제공하고 싶다면, modules = ["user.application.user_service"]
    로 선언하면 된다.
    """

    wiring_config = containers.WiringConfiguration(
        packages=["user", "note"],
    )
    """ 의존성을 제공할 모듈을 팩토리에 등록한다. """
    user_repo = providers.Factory(UserRepository)
    email_service = providers.Factory(EmailService)

    """ user_service를 제공할 펙토리를 제작함., 또한 의존성을 주입할 것을 user_repo라고 선언함. """
    user_service = providers.Factory(
        UserService, user_repo=user_repo, email_service=email_service
    )

    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)
