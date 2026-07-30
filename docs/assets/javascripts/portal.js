(() => {
  'use strict';

  const script = Array.from(document.scripts).find((item) => item.src.includes('/portal.js'));
  const assetsBase = script ? script.src.replace(/javascripts\/portal\.js.*$/, '') : '../../assets/';
  const dataUrl = (name) => `${assetsBase}data/${name}`;

  const labels = {
    en: {
      skills: 'Catalogued Skills', verified: 'Verified records', categories: 'Skill categories', benchmarkCategories: 'Benchmark categories',
      categoryDistribution: 'Skills by category', benchmarkSnapshot: 'Benchmark pipeline snapshot', search: 'Search by name, capability or tag',
      allCategories: 'All categories', name: 'Skill', category: 'Category', summary: 'Summary', status: 'Status', source: 'Source',
      noResults: 'No Skills match the selected filters.', updated: 'Data updated', synthetic: 'Synthetic benchmark data — pipeline demonstration only.',
      leader: 'Pipeline leader', models: 'ranked models'
    },
    pt: {
      skills: 'Skills catalogadas', verified: 'Registros verificados', categories: 'Categorias de Skills', benchmarkCategories: 'Categorias de benchmark',
      categoryDistribution: 'Skills por categoria', benchmarkSnapshot: 'Visão do pipeline de benchmarks', search: 'Buscar por nome, capacidade ou tag',
      allCategories: 'Todas as categorias', name: 'Skill', category: 'Categoria', summary: 'Resumo', status: 'Status', source: 'Fonte',
      noResults: 'Nenhuma Skill corresponde aos filtros selecionados.', updated: 'Dados atualizados', synthetic: 'Dados sintéticos de benchmark — apenas demonstração do pipeline.',
      leader: 'Líder do pipeline', models: 'modelos ranqueados'
    }
  };

  const loadJson = async (name) => {
    const response = await fetch(dataUrl(name), { cache: 'no-store' });
    if (!response.ok) throw new Error(`Unable to load ${name}: ${response.status}`);
    return response.json();
  };

  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };

  const titleCase = (value = '') => value
    .split(/[-_]/)
    .map((part) => part ? part[0].toUpperCase() + part.slice(1) : part)
    .join(' ');

  const uniqueRankedModels = (benchmarkData) => {
    const ids = new Set();
    Object.values(benchmarkData.categories || {}).forEach((category) => {
      (category.rankings || []).forEach((entry) => ids.add(entry.model_id));
    });
    return ids.size;
  };

  const makeKpi = (label, value, note = '') => {
    const card = el('div', 'cso-kpi');
    card.append(el('div', 'cso-kpi__label', label));
    card.append(el('div', 'cso-kpi__value', String(value)));
    if (note) card.append(el('div', 'cso-kpi__note', note));
    return card;
  };

  const renderDashboard = async (container) => {
    const lang = container.dataset.lang === 'pt' ? 'pt' : 'en';
    const t = labels[lang];

    try {
      const [skills, benchmarks] = await Promise.all([
        loadJson('skills.json'),
        loadJson('benchmarks.json')
      ]);

      const kpis = el('div', 'cso-kpis');
      kpis.append(
        makeKpi(t.skills, skills.total_skills ?? skills.skills?.length ?? 0, t.updated + ': ' + (skills.generated_on || '—')),
        makeKpi(t.verified, skills.verified_skills ?? 0),
        makeKpi(t.categories, skills.categories?.length ?? 0),
        makeKpi(t.benchmarkCategories, Object.keys(benchmarks.categories || {}).length, `${uniqueRankedModels(benchmarks)} ${t.models}`)
      );
      container.append(kpis);

      const grid = el('div', 'cso-grid');

      const distribution = el('section', 'cso-panel');
      distribution.style.gridColumn = 'span 7';
      const distributionHeader = el('div', 'cso-panel__header');
      const headerText = el('div');
      headerText.append(el('h2', '', t.categoryDistribution));
      headerText.append(el('p', '', `${skills.total_skills || 0} ${t.skills.toLowerCase()}`));
      distributionHeader.append(headerText);
      distribution.append(distributionHeader);

      const bars = el('div', 'cso-bars');
      const maximum = Math.max(1, ...(skills.categories || []).map((item) => item.count));
      (skills.categories || []).forEach((item) => {
        const row = el('div', 'cso-bar');
        const top = el('div', 'cso-bar__top');
        top.append(el('span', '', titleCase(item.id)), el('strong', '', String(item.count)));
        const track = el('div', 'cso-bar__track');
        const fill = el('div', 'cso-bar__fill');
        fill.style.width = `${Math.max(8, (item.count / maximum) * 100)}%`;
        track.append(fill);
        row.append(top, track);
        bars.append(row);
      });
      distribution.append(bars);

      const benchmarkPanel = el('section', 'cso-panel');
      benchmarkPanel.style.gridColumn = 'span 5';
      const benchmarkHeader = el('div', 'cso-panel__header');
      const benchmarkHeaderText = el('div');
      benchmarkHeaderText.append(el('h2', '', t.benchmarkSnapshot));
      benchmarkHeaderText.append(el('p', '', t.synthetic));
      benchmarkHeader.append(benchmarkHeaderText);
      benchmarkPanel.append(benchmarkHeader);

      Object.entries(benchmarks.categories || {}).forEach(([id, category]) => {
        const leader = category.rankings?.[0];
        const card = el('div', 'cso-card');
        card.style.gridColumn = '1 / -1';
        card.append(el('h3', '', category.label || titleCase(id)));
        card.append(el('p', '', leader ? `${t.leader}: ${leader.model_name} · ${leader.score}` : '—'));
        benchmarkPanel.append(card);
      });

      grid.append(distribution, benchmarkPanel);
      container.append(grid);

      const notice = el('p', 'cso-notice', benchmarks.data_notice || t.synthetic);
      container.append(notice);
    } catch (error) {
      container.append(el('div', 'cso-notice', error.message));
    }
  };

  const renderCatalog = async (container) => {
    const lang = container.dataset.lang === 'pt' ? 'pt' : 'en';
    const t = labels[lang];

    try {
      const data = await loadJson('skills.json');
      const skills = data.skills || [];

      const toolbar = el('div', 'cso-toolbar');
      const search = el('input', 'cso-control');
      search.type = 'search';
      search.placeholder = t.search;
      search.setAttribute('aria-label', t.search);

      const select = el('select', 'cso-control');
      const all = el('option', '', t.allCategories);
      all.value = '';
      select.append(all);
      [...new Set(skills.map((skill) => skill.category))].sort().forEach((category) => {
        const option = el('option', '', titleCase(category));
        option.value = category;
        select.append(option);
      });
      toolbar.append(search, select);
      container.append(toolbar);

      const meta = el('p', 'cso-meta');
      container.append(meta);

      const wrap = el('div', 'cso-table-wrap');
      const table = el('table', 'cso-table');
      const thead = el('thead');
      const headRow = el('tr');
      [t.name, t.category, t.summary, t.status, t.source].forEach((text) => headRow.append(el('th', '', text)));
      thead.append(headRow);
      const tbody = el('tbody');
      table.append(thead, tbody);
      wrap.append(table);
      container.append(wrap);

      const renderRows = () => {
        const query = search.value.trim().toLowerCase();
        const category = select.value;
        const filtered = skills.filter((skill) => {
          const searchable = [
            skill.display_name, skill.name, skill.category, skill.subcategory,
            ...(skill.capabilities || []), ...(skill.tags || [])
          ].join(' ').toLowerCase();
          return (!query || searchable.includes(query)) && (!category || skill.category === category);
        });

        tbody.replaceChildren();
        meta.textContent = `${filtered.length} / ${skills.length} · ${t.updated}: ${data.generated_on || '—'}`;

        if (!filtered.length) {
          const row = el('tr');
          const cell = el('td', 'cso-empty', t.noResults);
          cell.colSpan = 5;
          row.append(cell);
          tbody.append(row);
          return;
        }

        filtered.forEach((skill) => {
          const row = el('tr');

          const nameCell = el('td');
          nameCell.append(el('strong', '', skill.display_name));
          nameCell.append(document.createElement('br'));
          nameCell.append(el('code', '', skill.name));

          const categoryCell = el('td', '', titleCase(skill.category));
          const summaryCell = el('td', '', lang === 'pt' ? skill.summary_pt : skill.summary_en);

          const statusCell = el('td');
          const badge = el('span', `cso-badge cso-badge--${skill.status}`, titleCase(skill.status));
          statusCell.append(badge);

          const sourceCell = el('td');
          const link = el('a', '', t.source);
          link.href = skill.source_url;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          sourceCell.append(link);

          row.append(nameCell, categoryCell, summaryCell, statusCell, sourceCell);
          tbody.append(row);
        });
      };

      search.addEventListener('input', renderRows);
      select.addEventListener('change', renderRows);
      renderRows();
    } catch (error) {
      container.append(el('div', 'cso-notice', error.message));
    }
  };

  const initialize = () => {
    document.querySelectorAll('.cso-dashboard').forEach((node) => {
      if (!node.dataset.initialized) {
        node.dataset.initialized = 'true';
        renderDashboard(node);
      }
    });
    document.querySelectorAll('.cso-skills-catalog').forEach((node) => {
      if (!node.dataset.initialized) {
        node.dataset.initialized = 'true';
        renderCatalog(node);
      }
    });
  };

  document.addEventListener('DOMContentLoaded', initialize);
  document.addEventListener('DOMContentSwitch', initialize);
})();
