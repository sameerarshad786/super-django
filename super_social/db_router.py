class DatabaseRouter:
    """
    A router to control all database operations on models in the
    products and contenttypes applications.
    """

    route_app_labels = "products"

    def db_for_read(self, model, **hints):
        """
        Attempts to read products and contenttypes models go to supermarket.
        """
        if model._meta.model_name == "products":
            return "supermarket"
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write products and contenttypes models go to supermarket.
        """
        if model._meta.app_label == self.route_app_labels:
            return "supermarket"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the products or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.model_name == "products"
            or obj2._meta.model_name in "cart"
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the products and contenttypes apps only appear in the
        'supermarket' database.
        """
        if app_label in self.route_app_labels:
            return db == "supermarket"
        return None
