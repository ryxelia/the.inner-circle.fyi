from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse


from ticfyi.webring import get_web_ring_members


__all__: tuple[str, ...] = (
    "router",
)


router = APIRouter()


@router.get("/ring")
async def ring(request: Request) -> RedirectResponse:
    return RedirectResponse(
        url="/",
        status_code=HTTPStatus.FOUND,
    )


@router.get("/ring/next")
async def ring_next(request: Request, from_url: str | None = None) -> RedirectResponse:
    members = get_web_ring_members()
    if from_url is not None and from_url in members:
        current_index = members.index(from_url)
        next_index = (current_index + 1) % len(members)
        next_url = members[next_index]
        return RedirectResponse(
            url=URL(scheme="https", netloc=next_url),
            status_code=HTTPStatus.FOUND,
        )

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Invalid 'from_url' parameter. It must be one of the webring members.",
    )


@router.get("/ring/back")
async def ring_back(request: Request, from_url: str | None = None) -> RedirectResponse:
    members = get_web_ring_members()
    if from_url is not None and from_url in members:
        current_index = members.index(from_url)
        next_index = (current_index - 1) % len(members)
        next_url = members[next_index]
        return RedirectResponse(
            url=URL(scheme="https", netloc=next_url),
            status_code=HTTPStatus.FOUND,
        )

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Invalid 'from_url' parameter. It must be one of the webring members.",
    )


@router.get("/ring/go-to")
async def ring_go_to(request: Request, member: str | None = None) -> RedirectResponse:
    if member is not None and member in get_web_ring_members():
        return RedirectResponse(
            url=URL(scheme="https", netloc=member),
            status_code=HTTPStatus.FOUND,
        )

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail="Invalid 'member' parameter. It must be one of the webring members.",
    )
