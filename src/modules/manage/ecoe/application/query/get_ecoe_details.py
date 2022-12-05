from seedwork.domain.value_objects import UUID
from seedwork.application.queries import Query
from seedwork.application.query_handlers import QueryResult
from seedwork.application.decorators import query_handler

from modules.manage.ecoe.domain.repositories import EcoeRepository


class GetEcoeDetails(Query):
    ecoe_id: UUID


@query_handler
def get_ecoe_details(
    query: GetEcoeDetails, repository: EcoeRepository
) -> QueryResult:
    queryset = repository.session.query(repository.model).filter_by(
        id=query.ecoe_id
    )
    result = [dict(id=row.id, **row.data) for row in queryset.all()][0]
    return QueryResult.ok(result)
