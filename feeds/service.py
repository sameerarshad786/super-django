from .models import Comments, Remarks, Popularity


def get_replies(self: Comments, request):
    comments = Comments.objects.filter(on_comment=self)

    _comments = []
    popularity_details = []

    for comment in comments:
        total_replies = Comments.objects.filter(on_comment=comment.id).count()
        _remarks = Remarks.objects.filter(on_comment=comment.id)
        popularities = Remarks.objects.filter(
            on_post=comment.on_post.id, on_comment=comment.id
        )
        likes = popularities.filter(popularity=Popularity.LIKE)
        hearts = popularities.filter(popularity=Popularity.HEART)
        funny = popularities.filter(popularity=Popularity.FUNNY)
        insightful = popularities.filter(popularity=Popularity.INSIGHTFUL)
        disappoint = popularities.filter(popularity=Popularity.DISAPPOINT)
        current_user_action = popularities.filter(
            user=request.user
        ).values("popularity")
        _comments.append({
            "id": comment.id,
            "user_id": comment.user.id,
            "username": comment.user.profile.username,
            "email": comment.user.email,
            "profile_image": request.build_absolute_uri(
                comment.user.profile.profile_image.url
            ),
            "on_post": comment.on_post.id,
            "on_comment": comment.on_comment.id,
            "text": comment.text,
            "files": request.build_absolute_uri(
                comment.files.url
            ) if comment.files else None,
            "created": comment.created(),
            "updated": comment.updated(),
            "current_user_acrtion": current_user_action,
            "total_popularities": _remarks.count(),
            "popularity_count": {
                "likes": likes.count(),
                "hearts": hearts.count(),
                "funny": funny.count(),
                "insightful": insightful.count(),
                "disappoint": disappoint.count()
            },
            "popularity_details": popularity_details,
            "total_replies": total_replies,
            "child": get_replies(comment, request)
        })

        for remark in _remarks:
            popularity_details.append({
                "id": remark.id,
                "user_id": remark.user.id,
                "user_email": remark.user.email,
                "username": remark.user.profile.username,
                "profile_image": request.build_absolute_uri(
                    remark.user.profile.profile_image.url
                ),
                "on_comment": comment.id,
                "on_post": comment.on_post.id,
                "popularity": remark.popularity,
                "created_at": remark.created(),
                "updated_at": remark.updated()
            }),

    return _comments
