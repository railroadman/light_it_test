class MyNode(dict):
    def __init__(self, msg, root_parent_id, parent=0, user_id=None):

        self._parent = None
        self['root_parent_id'] = root_parent_id
        self['message'] = msg.comment_txt
        self['photo'] = msg.author.photo
        self['status'] = msg.status
        self['user_id'] = user_id
        self['author'] = msg.author.user.username
        if msg.author.user.pk == user_id:
            self['is_owner'] = 1
        else:
            self['is_owner'] = 0
        self['created_at'] = msg.created_at.strftime("%Y-%m-%d %H:%M")
        if parent == 0:
            self['id'] = msg.id
        if parent == 1:
            self['id'] = msg.parent_id
        self['childrens'] = []

    @property
    def parent(self):
        return self._parent

    def set_parent(self, node):
        self._parent = node

        node['childrens'].append(self)


def build_from_db(data, root_parent_id, user_id=None):
    lookup = {}
    for d in data:

        this = lookup.get(d.id)
        if this is None:
            this = MyNode(d, user_id=user_id, root_parent_id=root_parent_id)
            lookup[d.id] = this

        if d.id != d.parent_id:

            if lookup.has_key(d.parent_id) is True:
                parent = lookup[d.parent_id]
            else:
                # create parent, if missing
                parent = MyNode(d, parent=1, user_id=user_id, root_parent_id=root_parent_id)
                lookup[d.parent_id] = parent
            this.set_parent(parent)

    return lookup
