import unittest

from pyiron_workflow import Workflow

from pyiron_database.instance_database import (
    PostgreSQLInstanceDatabase,
    restore_node_from_database,
    restore_node_outputs,
    store_node_in_database,
    store_node_outputs,
)


@Workflow.wrap.as_function_node()
def AddNode(x: int = 1, y: int = 2) -> tuple[int, int]:
    a = x + y
    b = x - y
    return a, b


class TestPostgreSQL(unittest.TestCase):
    db: PostgreSQLInstanceDatabase

    def setUp(self):
        try:
            self.db = PostgreSQLInstanceDatabase(
                "postgresql://pyiron:pyiron@postgres/pyiron_workflow"
            )
        except ImportError as err:
            raise unittest.SkipTest("Skipping due to import error.") from err

    def test_idempotence_of_drop_init(self):
        self.db.drop()
        self.db.drop()
        self.db.init()
        self.db.init()

    def test_node_store_restore(self) -> None:
        node = AddNode(3, 4)

        self.db.drop()
        self.db.init()

        hash = store_node_in_database(
            self.db, node, store_outputs=False, store_input_nodes_recursively=True
        )

        node_restored = restore_node_from_database(self.db, hash)
        node_restored.run()
        self.assertEqual(node_restored.outputs.a.value, 7)
        self.assertEqual(node_restored.outputs.b.value, -1)


class TestOutputStorage(unittest.TestCase):
    def test_node_store_restore_outputs(self) -> None:
        node_to_store = AddNode(3, 4)
        node_to_store.run()
        store_node_outputs(node_to_store)

        node_to_restore = AddNode(3, 4)
        restore_node_outputs(node_to_restore)

        self.assertEqual(node_to_restore.outputs.a.value, node_to_store.outputs.a.value)
        self.assertEqual(node_to_restore.outputs.b.value, node_to_store.outputs.b.value)


if __name__ == "__main__":
    unittest.main()
