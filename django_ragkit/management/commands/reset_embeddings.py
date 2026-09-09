import random
from datetime import datetime

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.db import connection, transaction


class Command(BaseCommand):
    help = (
        "Backup, drop and recreate the QAEmbedding table "
        "using the current Django model definition."
    )

    APP_LABEL = "django_ragkit"
    MODEL_NAME = "QAEmbedding"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Starting QAEmbedding reset..."
            )
        )

        model = apps.get_model(
            self.APP_LABEL,
            self.MODEL_NAME,
        )

        table_name = model._meta.db_table

        self.stdout.write(
            f"Current table: {table_name}"
        )

        with transaction.atomic():

            # -------------------------------------------------
            # 1. Backup
            # -------------------------------------------------

            if self.table_exists(table_name):

                backup_table = self.create_backup_table_name()

                self.stdout.write(
                    self.style.WARNING(
                        f"Creating backup: {backup_table}"
                    )
                )

                self.backup_table(
                    source_table=table_name,
                    backup_table=backup_table,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Backup created: {backup_table}"
                    )
                )

                # -------------------------------------------------
                # 2. Drop old table
                # -------------------------------------------------

                self.stdout.write(
                    self.style.WARNING(
                        f"Dropping table: {table_name}"
                    )
                )

                self.delete_model(model)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Dropped table: {table_name}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.NOTICE(
                        f"Table '{table_name}' does not exist."
                    )
                )

            # -------------------------------------------------
            # 3. Create new table using current Django model
            # -------------------------------------------------

            self.stdout.write(
                self.style.WARNING(
                    "Creating new QAEmbedding table..."
                )
            )

            self.create_model(model)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created table: {table_name}"
                )
            )

        # -----------------------------------------------------
        # 4. Make migrations
        # -----------------------------------------------------

        self.stdout.write(
            self.style.WARNING(
                "Running makemigrations..."
            )
        )

        call_command("makemigrations")

        # -----------------------------------------------------
        # 5. Apply migrations
        # -----------------------------------------------------

        self.stdout.write(
            self.style.WARNING(
                "Running migrate..."
            )
        )

        call_command("migrate")

        self.stdout.write(
            self.style.SUCCESS(
                "QAEmbedding reset completed successfully."
            )
        )

    # =========================================================
    # Database helpers
    # =========================================================

    def table_exists(self, table_name: str) -> bool:
        """
        Check whether a PostgreSQL table exists.
        """

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = %s
                )
                """,
                [table_name],
            )

            return cursor.fetchone()[0]

    def create_backup_table_name(self) -> str:
        """
        Generate a unique backup table name.

        Example:
            qaembedding_backup_20260909_4821
        """

        date = datetime.now().strftime("%Y%m%d")

        while True:

            random_number = random.randint(1000, 9999)

            backup_table = (
                f"qaembedding_backup_{date}_{random_number}"
            )

            if not self.table_exists(backup_table):
                return backup_table

    def backup_table(
        self,
        source_table: str,
        backup_table: str,
    ):
        """
        Backup the table structure and data.

        Indexes are not copied because this is an archive
        and should not be used for active vector search.
        """

        source = connection.ops.quote_name(source_table)
        backup = connection.ops.quote_name(backup_table)

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE {backup}
                AS TABLE {source}
                """
            )

    def delete_model(self, model):
        """
        Delete the model table using Django's schema editor.
        """

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(model)

    def create_model(self, model):
        """
        Create the model table using the current Django model.

        This means the current VectorField dimension and indexes
        from Meta will be used.
        """

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(model)