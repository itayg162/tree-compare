tree_a = {
    "id": "1", "name": "Company", "type": "root", "children": [
        {"id": "2", "name": "Engineering", "type": "department", "children": [
            {"id": "4", "name": "Dev Team", "type": "team", "children": []}
        ]},
        {"id": "3", "name": "HR", "type": "department", "children": []}
    ]
}

tree_b = {
    "id": "1", "name": "Company", "type": "root", "children": [
        {"id": "2", "name": "Engineering", "type": "department", "children": [
            {"id": "5", "name": "QA Team", "type": "team", "children": []}
        ]},
        {"id": "6", "name": "Marketing", "type": "department", "children": []}
    ]
}

tree_a_no_id = {
    "name": "Company", "type": "root", "children": [
        {"name": "Engineering", "type": "department", "children": [
            {"name": "Dev Team", "type": "team", "children": []}
        ]},
        {"name": "HR", "type": "department", "children": []}
    ]
}

tree_b_no_id = {
    "name": "Company", "type": "root", "children": [
        {"name": "Engineering", "type": "department", "children": [
            {"name": "QA Team", "type": "team", "children": []}
        ]},
        {"name": "Marketing", "type": "department", "children": []}
    ]
}

tree_a_complex = {
    "id": "root", "name": "Acme Corp", "type": "company", "children": [
        {"id": "dep1", "name": "Engineering", "type": "department", "children": [
            {"id": "team1", "name": "Platform Team", "type": "team", "children": [
                {"id": "emp1", "name": "Alice", "type": "employee"},
                {"id": "emp2", "name": "Bob", "type": "employee"}
            ]},
            {"id": "team2", "name": "ML Team", "type": "team", "children": [
                {"id": "emp3", "name": "Charlie", "type": "employee"}
            ]}
        ]},
        {"id": "dep2", "name": "HR", "type": "department", "children": [
            {"id": "emp4", "name": "Diana", "type": "employee"}
        ]}
    ]
}

tree_b_complex = {
    "id": "root", "name": "Acme Corp", "type": "company", "children": [
        {"id": "dep1", "name": "Engineering", "type": "department", "children": [
            {"id": "team1", "name": "Platform Team", "type": "team", "children": [
                {"id": "emp1", "name": "Alice", "type": "employee"},
                {"id": "emp5", "name": "Eve", "type": "employee"}
            ]},
            {"id": "team3", "name": "Infra Team", "type": "team", "children": []}
        ]},
        {"id": "dep3", "name": "Marketing", "type": "department", "children": []}
    ]
}

tree_a_ui = {
  "id": "root",
  "name": "Acme Corp",
  "type": "company",
  "children": [
    {
      "id": "dep1",
      "name": "Engineering",
      "type": "department",
      "children": [
        {
          "id": "team1",
          "name": "Platform Team",
          "type": "team",
          "children": [
            { "id": "emp1", "name": "Alice", "type": "employee" },
            { "id": "emp2", "name": "Bob", "type": "employee" }
          ]
        }
      ]
    }
  ]
}

tree_b_ui = {
  "id": "root",
  "name": "Acme Corp",
  "type": "company",
  "children": [
    {
      "id": "dep1",
      "name": "Engineering",
      "type": "department",
      "children": [
        {
          "id": "team1",
          "name": "Platform Team",
          "type": "team",
          "children": [
            { "id": "emp1", "name": "Alice", "type": "employee" },
            { "id": "emp3", "name": "Charlie", "type": "employee" }
          ]
        },
        {
          "id": "team2",
          "name": "Infra Team",
          "type": "team",
          "children": []
        }
      ]
    }
  ]
}
