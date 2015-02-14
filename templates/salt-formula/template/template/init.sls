{{'{%'}} from "{{formula_name}}/map.jinja" import {{formula_name}} with context {{'%}'}}

{{formula_name}}:
  pkg:
    - installed
    - name: {{'{{'}} {{formula_name}}.pkg {{'}}'}}
  service:
    - running
    - name: {{'{{'}} {{formula_name}}.service {{'}}'}}
    - enable: True
