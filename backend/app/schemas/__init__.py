from app.schemas.auth import AccessToken, LoginRequest, RefreshRequest, TokenPair  # noqa: F401
from app.schemas.common import Message, Paginated  # noqa: F401
from app.schemas.media import MediaAltUpdate, MediaOut, MediaUploadResponse  # noqa: F401
from app.schemas.news import (  # noqa: F401
    CategoryAdminOut,
    CategoryCreate,
    CategoryPublicOut,
    CategoryUpdate,
    NewsAdminOut,
    NewsCreate,
    NewsPublicDetail,
    NewsPublicListItem,
    NewsStats,
    NewsUpdate,
)
from app.schemas.page import (  # noqa: F401
    StaticPageAdminOut,
    StaticPageCreate,
    StaticPageNavItem,
    StaticPagePublicOut,
    StaticPageUpdate,
)
from app.schemas.seo import (  # noqa: F401
    GlobalSEOItem,
    GlobalSEOUpdate,
    RedirectCreate,
    RedirectOut,
    RedirectUpdate,
)
from app.schemas.stats import ActivityItem, StatsOverview, TopNewsItem  # noqa: F401
from app.schemas.user import UserCreate, UserOut, UserUpdate  # noqa: F401
