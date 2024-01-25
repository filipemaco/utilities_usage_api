from rest_framework.test import APIRequestFactory, force_authenticate


def request_factory(view_set, user, url, method=None, data=None, pk=None):
    factory = APIRequestFactory()
    if method == 'post':
        request = factory.post(url, data, format='json')
        view = view_set.as_view({method: 'create'})
    elif method == 'delete':
        request = factory.delete(url, format='json')
        view = view_set.as_view({method: 'destroy'})
    elif method == 'put':
        request = factory.put(url, data, format='json')
        view = view_set.as_view({method: 'update'})
    elif method == 'patch':
        request = factory.patch(url, data, format='json')
        view = view_set.as_view({method: 'partial_update'})
    else:
        request = factory.get(url, format='json')
        view = view_set.as_view({'get': 'list'})

    force_authenticate(request, user=user)
    return view(request, pk=pk)
