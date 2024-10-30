from dependency_injector import containers, providers
from fastyr.infrastructure.database.connection import create_session_factory
from fastyr.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository
from fastyr.services.providers.pipeline_service import PipelineService

class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    config = providers.Configuration()
    
    # Database
    db_session_factory = providers.Singleton(
        create_session_factory,
        url=config.db.url
    )
    
    # Repositories
    audio_process_repository = providers.Factory(
        SQLAlchemyRepository,
        session=db_session_factory,
    )
    
    # Services
    pipeline_service = providers.Factory(
        PipelineService,
        repository=audio_process_repository,
    ) 