let context = #{};

// Create project prefix variations
context += prompt("Project Prefix:", "project-prefix", #{
    placeholder: "Customer Chat",
    help: "Project Name",
    cases: [
        CasedIdentityCasedValue(PROGRAMMING_CASES),
    ],
});

context += prompt("App name:", "app-name", #{
    cases: [
        CasedIdentityCasedValue(PROGRAMMING_CASES),
        FixedKeyCasedValue("ProjectTitle", TitleCase),
    ],
});

context += prompt("Chatbot port:", "chatbot-port", #{
    placeholder: "Customer Chat",
    defaults_with: "8501",
});

if ANSWERS.menus != () {
    for menu in ANSWERS.menus {  // get an array of all the property names via 'keys'
        if menu["select_type"] == "single" {
            context += prompt(menu["menu_name"] + ":", menu["menu_name"], #{
                    help: "Project Features",
                    type: Select(menu["menu_options"] + ["None"]),
                });
        } else {
            context += prompt(menu["menu_name"] + ":", menu["menu_name"], #{
                help: "Project Features",
                type: MultiSelect(menu["menu_options"]),
            });
        }
    }
}

// Create case variations for the combined project prefix and suffix
context += set("project-name", render("{{ project-prefix }}-{{ app-name }}", context), #{
    cases: [
        CasedIdentityCasedValue(PROGRAMMING_CASES),
        FixedKeyCasedValue("ProjectTitle", TitleCase),
    ],
});



// Generate content
render(Directory("content/base"), context,
    #{
        if_exists: Overwrite,
    });

render(Archetype("manifests"), context["project-name"], context +
    #{
        "persistence": "None",
        if_exists: Overwrite,
    }
);
render(Archetype("gitignore"), context["project-name"],
    #{
        "ignore": ["python"],
        if_exists: Overwrite,
    }
);


