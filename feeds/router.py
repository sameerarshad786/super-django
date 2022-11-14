from rest_framework.routers import DefaultRouter

from .views import feeds_view, comments_view, remarks_view


router = DefaultRouter()


router.register(
    r"post", feeds_view.FeedViewSets, basename="posts-crud"
    )
router.register(
    r"comment", comments_view.CommentViewSets, basename="comments-crud"
    )
router.register(
    r"remark", remarks_view.RemarkViewSets, basename="remarks-crud"
    )
