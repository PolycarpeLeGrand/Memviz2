import pandas as pd
from collections import defaultdict
from enum import Enum, auto
import codecs
import pickle
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Union, Optional, Iterable


class DType(Enum):
    DF = auto()
    MD = auto()
    CSV = auto()
    PICKLE = auto()


@dataclass
class SavedData:
    name: str
    path: Union[str, Path]
    d_type: Optional[DType] = DType.PICKLE
    details: Optional[str] = ''
    orient: Optional[str] = ''
    loaded: Optional[bool] = False

    def __str__(self) -> str:
        return f'[{self.d_type}] {self.name} {self.details}'


class DataManager:
    """Use this to store the data used by the project in one convenient object.

    This class helps keep things tidy by loading and organizing the loaded data. Using a DataManager to handle the data
    will make things easier when working with many files, removing the need to set and import a bunch of variables.

    Names and paths for data of different types can be defined in config.py. A DataManager object can then be created
    and the data loaded in init.

    Variables are named after the values specified in config. For instance, {'name': 'TEST_DF', ...} will be loaded as
    dm.TEST_DF.

    TODO __str__ __repr__

    Args:
        sd_list (Iterable[SavedData]): A list of SavedData objects to be loaded, usually imported from config.py.
        save_doc_md (Optional[bool]): Whether to save the doc markdown to /DATA_DOC.md. Defaults to True.
        load_readme (Optional[bool]): Whether to load README.md as a SavedData.

    Attributes:
        loaded_data_info (defaultdict[DType, list[SavedData]]): Dict tracking the loaded SavedData objects. Defaultdict
            with DTypes as keys and lists of SavedData objects as values. SavedData objects hold only the metadata,
            the data itself is added to new attributes via setattr.

        DOC_MD (str): Markdown string giving an overview of all the loaded data.

    """

    def __init__(self,
                 sd_list: Iterable[SavedData],
                 save_doc_md: Optional[bool] = True,
                 load_readme: Optional[bool] = True):

        self.loaded_data_info: defaultdict[DType, list[SavedData]] = defaultdict(list)

        for sd in sd_list:
            self.load_saved_data(sd)

        if load_readme:
            self.load_saved_data(SavedData(name='README_MD', d_type=DType.MD, path='README.md'))

        self.DOC_MD: str = self.make_doc_markdown()

        if save_doc_md:
            with open('DATA_DOC.md', 'w') as f:
                #f.write(self.DOC_MD)
                pass

    def load_saved_data(self, sd: SavedData):
        """Loads and assigns a single SavedData object to an instance variable"""

        if hasattr(self, sd.name):
            print(f'Variable "{sd.name}" already exists in DataManager, value will be overwritten. Check for duplicates!')

        try:
            if sd.d_type == DType.DF:
                d = pd.read_pickle(sd.path)
            elif sd.d_type == DType.MD:
                with codecs.open(sd.path, 'r', 'utf-8') as f:
                    d = f.read()
            elif sd.d_type == DType.CSV:
                with open(sd.path, newline='') as f:
                    # TODO Manage orient
                    d = {n[0]: [n[i + 1] for i in range(len(n) - 1) if n[i + 1] != ''] for n in csv.reader(f)}
            else:
                d = pickle.load(open(sd.path, 'rb'))
            setattr(self, sd.name, d)
            sd.loaded = True
            self.loaded_data_info[sd.d_type].append(sd)

        except Exception:
            print(f'DataManager error: Could not load {sd.d_type} with name {sd.name}')

    def make_doc_markdown(self, n_enum: int = 10, max_chars: int = None) -> str:
        doc = f'Loaded Data Doc\n=====\nTotal loaded objects: {sum(len(v) for v in self.loaded_data_info.values())}\n' + '\n'.join(f'* {k}: {len(v)}' for k, v in self.loaded_data_info.items()) + '\n\n'

        doc += '\nDataframes\n----\n'
        for sd in self.loaded_data_info[DType.DF]:
            df = getattr(self, sd.name)
            doc += f"""
\n**{sd.name}**\n
{sd.details}\n
Dimensions: {len(df.index)} rows X {len(df.columns)} columns.  
Memory usage: {df.memory_usage(deep=True).sum() / (1024 ** 2):.3f} mb  
Rows (first {n_enum}): {', '.join(str(i) for i in df.index.values[:n_enum])}  
Columns (first {n_enum}): {', '.join(str(i) for i in df.columns.values[:n_enum])}\n\n
Shuffled sample:\n
<div class="table-wrapper">{df.sample(10).iloc[:, :50].to_html()}</div>\n
&nbsp
"""

        doc += '\nCsv files (loaded as dicts)\n----\n'
        for sd in self.loaded_data_info[DType.CSV]:
            csv = getattr(self, sd.name)
            doc += f"""
\n**{sd.name}**\n
{sd.details}\n
Num labels: {len(csv)}. Max num values: {max(len(v) for v in csv.values())}. Total values: {sum(len(v) for v in csv.values())}  
Labels (first {n_enum}): {', '.join(str(i) for i in csv.keys()[:n_enum])}\n
&nbsp
"""

        doc += '\nMarkdowns\n----\n'
        for sd in self.loaded_data_info[DType.MD]:
            md = getattr(self, sd.name)
            doc += f"""
\n**{sd.name}**\n
{sd.details}\n
Length: {len(md)} characters / {len(md.split(' '))} words.\n\n
```markdown\n{md.replace('`', '^')[:max_chars]}\n```
&nbsp
"""

        doc += '\nPickled objects\n----\n'
        for sd in self.loaded_data_info[DType.PICKLE]:
            p = getattr(self, sd.name)
            doc += f"""
\n**{sd.name}**\n
{sd.details}\n
Type: {type(p)}  
Str value (first {150} characters): {str(p)[:150]}...\n
&nbsp
"""

        return doc
