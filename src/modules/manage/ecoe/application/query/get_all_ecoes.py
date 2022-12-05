from seedwork.domain.value_objects import UUID
from seedwork.application.queries import Query
from seedwork.application.query_handlers import QueryResult
from seedwork.application.decorators import query_handler
from modules.manage.ecoe.domain.repositories import EcoeRepository


class GetAllEcoes(Query):
    ...


@query_handler
def get_all_ecoes(
    query: GetAllEcoes, repository: EcoeRepository
) -> QueryResult:
    queryset = repository.session.query(repository.model)
    result = [dict(id=row.id, **row.data) for row in queryset.all()]
    # TODO: add error handling
    return QueryResult.ok(result)
