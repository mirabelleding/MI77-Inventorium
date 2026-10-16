# Pandas Advanced Methods — Comprehensive Study Notes

**Reference style:** method/function → what it does, with distinctions, examples and application notes.  
**Coverage:** DataFrame, Series, GroupBy, `.str`, `.dt`, Index/MultiIndex, time-series, windowing, IO, testing and top-level `pd` functions.  
**Version guidance:** The original guide was written around Pandas 3.0.x. Some features also work in 2.x; verify version-specific behavior. For example, `DataFrame.map()` is the elementwise method replacing the older `applymap()`, and `DataFrame.mad()` is no longer part of current Pandas. An API marked *historical* is included to preserve the full original study map, not recommended for new code.

> **Mental model:** know which *operation* you need (filter, align, aggregate, transform, reshape, compare) before choosing the exact method.

## 1. Row filtering / boolean selection

```text
query()                 filter rows using expression syntax
isin()                  test membership against a collection
between()               test whether values fall inside a range
where()                 keep values where condition is True
mask()                  replace values where condition is True

any()                   True if any value satisfies condition
all()                   True if all values satisfy condition

filter()                select rows/columns by label patterns
take()                  select rows/columns by integer positions
truncate()              restrict rows before/after index bounds

head()                  first n rows
tail()                  last n rows
sample()                random sample of rows
nlargest()               rows containing n largest values
nsmallest()              rows containing n smallest values
```

**Distinction:**

```text
where(cond)             preserve values where cond == True
mask(cond)              replace values where cond == True
```

Examples:

```python
df.query("division == 'CB' and stage == 1")
df[df['currency'].isin(['CAD', 'USD'])]
df[df['value'].between(100, 500)]
df['value'].where(df['value'] >= 0, other=0)
df['value'].mask(df['value'] < 0, other=0)
df.filter(regex='^measure_')
df.nlargest(5, 'value')
```

`Series.between()` includes the bounds by default; `DataFrame.filter()` filters **labels**, not cell values.

## 2. Column creation / mutation

```text
assign()                 create/replace columns declaratively
insert()                 insert column at specific position
pop()                    remove column and return it
drop()                   remove rows or columns

rename()                 rename columns/index labels
rename_axis()            rename index/column axis itself

add_prefix()             prepend text to column/index names
add_suffix()             append text to column/index names

update()                 overwrite values from another DataFrame
replace()                replace specific values/patterns

set_axis()               replace entire index/columns axis
```

```python
df.assign(
    revenue=lambda x: x['price'] * x['quantity'],
    margin=lambda x: x['revenue'] - x['cost'],
)
```

`assign()` evaluates keyword expressions **left-to-right**: later assignments can reference earlier new columns.

```python
df.insert(0, 'source', 'upload')
df.rename(columns={'keyid': 'transaction_id'})
df.add_prefix('input_')
```

## 3. Function application

```text
apply()                  apply function across rows/columns
map()                    elementwise transformation
Series.map()             map values using dict/Series/function
agg()                    aggregate using one/multiple functions
aggregate()              alias of agg()
transform()              return transformed same-sized result
pipe()                   pass object through custom function
```

```text
apply()                  operate on Series/rows/columns
map()                    operate on individual values
agg()                    many values → summary value(s)
transform()              many values → same-shape result
pipe()                   DataFrame → arbitrary function
```

`Series.map()` accepts a dict, Series or callable; `DataFrame.map()` applies a scalar function elementwise. Example:

```python
df['stage_label'] = df['stage'].map({1: 'Stage 1', 2: 'Stage 2'})
df['normalized'] = df['value'].transform(lambda s: s - s.mean())
df.pipe(lambda x: x.dropna(subset=['keyid']))
```

## 4. GroupBy — core methods

```text
groupby()                split data into groups

groupby().agg()          aggregate groups
groupby().aggregate()    same as agg()
groupby().transform()    group calculation preserving rows
groupby().apply()        arbitrary operation per group
groupby().filter()       retain/remove entire groups

groupby().get_group()    retrieve one group
groupby().groups         mapping of group → labels
groupby().indices        mapping of group → row positions
```

**Mental model:** aggregation collapses group rows; transformation preserves group row alignment; application is flexible; filtering keeps or discards **whole groups**.

```python
df.groupby('stage')['value'].agg(['sum', 'mean'])
df['group_total'] = df.groupby('stage')['value'].transform('sum')
df.groupby('stage').filter(lambda g: len(g) >= 3)
df.groupby('stage').get_group(1)
```

## 5. GroupBy — aggregations

```text
groupby().sum()          group sums
groupby().mean()         group means
groupby().median()       group medians
groupby().min()          group minima
groupby().max()          group maxima

groupby().count()        non-null count
groupby().size()         number of rows including nulls
groupby().nunique()      unique count

groupby().std()          group standard deviation
groupby().var()          group variance
groupby().sem()          standard error
groupby().quantile()     group quantiles

groupby().prod()         group products

groupby().first()        first non-null value
groupby().last()         last non-null value
groupby().nth()          nth row/value

groupby().any()          whether any values are True
groupby().all()          whether all values are True

groupby().idxmax()       index of group maximum
groupby().idxmin()       index of group minimum
```

```python
df.groupby(['division', 'stage']).agg(
    total=('value', 'sum'),
    rows=('keyid', 'size'),
    unique_ids=('hierarchy_id', 'nunique'),
)
df.groupby('stage').nth(1)  # second row of each group (positional)
```

## 6. GroupBy — row-preserving operations

```text
groupby().cumcount()     row number within each group
groupby().ngroup()       numeric ID for each group

groupby().cumsum()       cumulative sum within group
groupby().cumprod()      cumulative product
groupby().cummax()       cumulative maximum
groupby().cummin()       cumulative minimum

groupby().rank()         rank within groups
groupby().shift()        shift within groups
groupby().diff()         difference within groups
groupby().pct_change()   fractional change within groups

groupby().ffill()        forward-fill within groups
groupby().bfill()        backward-fill within groups

groupby().head()         first n rows of each group
groupby().tail()         last n rows of each group
groupby().sample()       sample rows within groups
```

These often eliminate expensive/custom `groupby().apply()`.

```python
df['sequence'] = df.groupby('transaction_id').cumcount()
df['previous_value'] = df.groupby('hierarchy_id')['value'].shift()
```

## 7. Reshaping

```text
melt()                   wide → long
pivot()                  long → wide
pivot_table()            pivot + aggregation

stack()                  columns → inner row index
unstack()                inner row index → columns

explode()                list-like cell → multiple rows
transpose() / T          rows ↔ columns
wide_to_long()           structured wide → long conversion
crosstab()               frequency / contingency table
```

```text
pivot()                  requires unique index/column pairs
pivot_table()            permits duplicates by aggregating
```

```python
df.melt(id_vars=['hierarchy_id'], var_name='month', value_name='value')
long_df.pivot(index='hierarchy_id', columns='month', values='value')
long_df.pivot_table(index='hierarchy_id', columns='month', values='value', aggfunc='sum')
df.explode('measure_types')
pd.crosstab(df['division'], df['stage'])
```

## 8. Combining DataFrames

```text
merge()                  database-style join
join()                   primarily index-based join
concat()                 stack/combine objects along an axis

combine()                combine using custom element function
combine_first()          fill nulls using another DataFrame

update()                 overwrite values from another DataFrame
align()                  align two objects to matching axes
```

```text
merge()                  SQL JOIN
concat(axis=0)           UNION ALL / append rows
concat(axis=1)           place columns side-by-side
align()                  synchronize indexes before calculation
combine_first()          COALESCE-like behavior
```

```python
left.merge(right, on='keyid', how='left', validate='one_to_one')
pd.concat([df_a, df_b], ignore_index=True)
left.combine_first(right)  # fill missing left cells from right
left, right = left.align(right, join='outer', axis=None)
```

`concat()` is only *analogous* to SQL `UNION ALL`: it does not automatically enforce SQL-style column/type semantics.

## 9. Duplicate handling

```text
duplicated()             identify duplicate rows/values
drop_duplicates()        remove duplicates
unique()                 unique values (Series)
nunique()                number of unique values
value_counts()           frequency of each value
factorize()              values → integer codes + uniques
mode()                   most frequent value(s)
```

```python
df.duplicated(
    subset=['scope_id', 'stage', 'month_date'],
    keep=False,
)
```

`keep=False` flags **every** row belonging to a duplicate key group, not only the later occurrences.

## 10. Missing-data operations

```text
isna()                   detect missing values
isnull()                 alias of isna()
notna()                  detect non-missing values
notnull()                alias of notna()
dropna()                 remove missing rows/columns
fillna()                 fill missing values
ffill()                  forward-fill
bfill()                  backward-fill
interpolate()            estimate intermediate missing values
first_valid_index()      first non-null index
last_valid_index()       last non-null index
```

```python
df.dropna(subset=['keyid'])
df.dropna(how='all')
df.dropna(thresh=3)
df.ffill(limit=2)
```

## 11. Sorting

```text
sort_values()            sort by column values
sort_index()             sort by index
nlargest()               highest n records
nsmallest()              lowest n records
rank()                   calculate rankings
```

`rank(method=...)` supports:

```text
method='average'
method='min'
method='max'
method='first'
method='dense'
```

```python
df.sort_values(['division', 'month_date'])
df['value'].rank(method='dense', ascending=False)
```

## 12. Index manipulation

```text
set_index()              columns → index
reset_index()            index → columns
reindex()                conform object to specified labels
reindex_like()           conform to another object's axes
rename_axis()            name the index/column axis
set_axis()               replace index/column labels
sort_index()             sort index
droplevel()              remove MultiIndex level
swaplevel()              swap MultiIndex levels
reorder_levels()         reorder MultiIndex levels
xs()                     cross-section of MultiIndex
take()                   positional selection
```

```python
df.xs(
    ('CB', 'Stage1'),
    level=['division', 'stage'],
)
```

`xs()` is a concise way to select a **MultiIndex cross-section** instead of verbose `.loc[]` expressions.

## 13. Index inspection

```text
Index.isin()                 membership test
Index.duplicated()           duplicate labels
Index.drop_duplicates()      unique labels
Index.unique()               unique labels
Index.get_loc()              position of particular label
Index.get_indexer()          positions for multiple labels
Index.intersection()         common labels
Index.union()                union of labels
Index.difference()           labels only in one index
Index.symmetric_difference() labels unique to either index
Index.equals()               exact index equality
```

```python
missing_ids = expected.index.difference(actual.index)
shared_ids = expected.index.intersection(actual.index)
```

## 14. Selection helpers (indexers rather than ordinary methods)

```text
loc[]                    label-based selection
iloc[]                   positional selection
at[]                     fast scalar selection by label
iat[]                    fast scalar selection by position
xs()                     MultiIndex cross-section
```

```text
loc[row_labels, columns]
iloc[row_positions, column_positions]
at[row_label, column]
iat[row_position, column_position]
```

```python
df.loc[df['stage'] == 1, ['keyid', 'value']]
df.iloc[:10, :3]
df.at[100, 'value']
df.iat[0, 1]
```

## 15. Data types

```text
astype()                 explicitly cast dtype
convert_dtypes()         infer best nullable Pandas dtypes
infer_objects()          infer better types for object columns
select_dtypes()          choose columns based on dtype
to_numeric()             values → numeric
to_datetime()            values → datetime
to_timedelta()           values → timedelta
```

```python
df.select_dtypes(include='number')
df.select_dtypes(include=['string', 'object'])
df.convert_dtypes()
pd.to_numeric(df['value'], errors='coerce')
```

**Note:** `to_numeric`, `to_datetime`, and `to_timedelta` here refer to top-level `pd.to_*` functions.

## 16. Numeric descriptive statistics

```text
sum()                    sum
mean()                   arithmetic mean
median()                 median
min()                    minimum
max()                    maximum
std()                    standard deviation
var()                    variance
sem()                    standard error
quantile()               arbitrary quantile
mode()                   mode
count()                  non-null count
prod()                   product
mad()                    historical mean absolute deviation *
```

`mad()` is included because it appeared in the original notes, but is **historical/removed from recent Pandas**; use an explicit expression when needed:

```python
s = df['value']
mean_absolute_deviation = (s - s.mean()).abs().mean()
```

## 17. Statistical relationships

```text
corr()                   pairwise correlation
cov()                    covariance
corrwith()               correlate against another object
autocorr()               Series autocorrelation
```

```python
df.corr(numeric_only=True)
df['value'].autocorr(lag=1)
```

## 18. Location statistics

```text
idxmax()                 index of maximum
idxmin()                 index of minimum
nlargest()               largest n
nsmallest()              smallest n
quantile()               percentile/quantile
rank()                   ordinal rankings
```

Instead of selecting all equal-to-max rows:

```python
df[df['x'] == df['x'].max()]
```

If you only need the **index label**:

```python
df['x'].idxmax()
```

## 19. Cumulative operations

```text
cumsum()                 cumulative sum
cumprod()                cumulative product
cummax()                 cumulative maximum
cummin()                 cumulative minimum

groupby().cumsum()       groupwise cumulative sum
groupby().cumprod()      groupwise cumulative product
groupby().cummax()       groupwise cumulative max
groupby().cummin()       groupwise cumulative min
```

## 20. Difference / change operations

```text
diff()                   difference from previous row
pct_change()             fractional change
shift()                  shift rows forward/backward
```

```python
df['previous_month'] = (
    df.groupby(['hierarchy_id', 'measure_type'])['value']
      .shift(1)
)
df['change'] = (
    df.groupby('hierarchy_id')['value']
      .diff()
)
```

**Note:** `pct_change()` is fractional (e.g. `0.05` means 5%); multiplying by 100 gives a percentage figure.

## 21. Arithmetic methods

```text
add()                    +
sub()                    -
mul()                    *
div()                    /
truediv()                /
floordiv()               //
mod()                    %
pow()                    **
radd()                   reversed +
rsub()                   reversed -
rmul()                   reversed *
rdiv()                   reversed /
rpow()                   reversed **
```

**Why use the method form?** Index alignment plus optional `fill_value`:

```python
a.add(b, fill_value=0)   # unlike plain a + b
```

## 22. Comparison methods

```text
eq()                     ==
ne()                     !=
gt()                     >
ge()                     >=
lt()                     <
le()                     <=
```

```python
df['A'].eq(df['B'])
# Equivalent to (when indexes match):
df['A'] == df['B']
```

Method form can be clearer in chains and exposes alignment-related options.

## 23. DataFrame comparison

```text
equals()                 determine exact object equality
compare()                show element-by-element differences
```

```text
equals()                 returns True / False
compare()                returns differences
```

```python
expected.compare(actual)
```

`compare()` requires identically labeled axes; align/sort the inputs as appropriate before comparison.

## 24. String operations — matching/searching

Vectorized string operations are under the `.str` accessor.

```text
str.contains()           substring/regex exists
str.startswith()         begins with text
str.endswith()           ends with text
str.match()              regex matches beginning
str.fullmatch()          regex matches entire string
str.extract()            extract first regex match groups
str.extractall()         extract every regex match
str.findall()            return all regex matches
str.count()              count regex occurrences
```

`str.fullmatch()` is useful in validation because the **entire string** must satisfy the regex; `str.extract()` can turn capture groups into columns.

```python
df['code'].str.fullmatch(r'[A-Z]{2}-\d{4}')
df['code'].str.extract(r'(?P<division>[A-Z]{2})-(?P<id>\d{4})')
```

## 25. String operations — cleanup

```text
str.lower()              lowercase
str.upper()              uppercase
str.title()              Title Case
str.capitalize()         capitalize first character
str.casefold()           aggressive Unicode lowercase
str.swapcase()           swap case
str.strip()              trim both ends
str.lstrip()             trim left
str.rstrip()             trim right
str.replace()            replace text/regex
str.removeprefix()       remove prefix
str.removesuffix()       remove suffix
str.normalize()          Unicode normalization
```

```python
df['code'].str.strip().str.upper()
df['name'].str.replace(r'\s+', ' ', regex=True)
```

## 26. String operations — splitting / combining

```text
str.split()              split string → lists/columns
str.rsplit()             split from right
str.partition()          split around first separator
str.rpartition()         split around last separator
str.cat()                concatenate strings
str.join()               join iterable contents
str.get()                get element at position
str.slice()              substring slicing
str.slice_replace()      replace substring slice
```

```python
df['code'].str.split('-', expand=True)
```

## 27. String operations — formatting

```text
str.len()                string length
str.pad()                pad strings
str.center()             center strings
str.ljust()              left justify
str.rjust()              right justify
str.zfill()              zero-pad
str.wrap()               wrap long strings
str.repeat()             repeat strings
```

```python
df['id'].astype('string').str.zfill(8)
```

`zfill()` left-pads with zeros to a target width.

## 28. String classification

```text
str.isalpha()            alphabetic
str.isnumeric()          numeric characters
str.isdigit()            digits
str.isdecimal()          decimal characters
str.isalnum()            alphanumeric
str.isspace()            whitespace
str.islower()            lowercase
str.isupper()            uppercase
str.istitle()            title case
```

These are handy for import/data-validation checks.

## 29. Datetime — component extraction (properties)

```text
dt.year                   year
dt.month                  month
dt.day                    day
dt.hour                   hour
dt.minute                 minute
dt.second                 second
dt.microsecond            microsecond
dt.dayofweek              weekday number
dt.weekday                alias
dt.dayofyear              day number in year
dt.day_name()             weekday name, e.g. 'Monday'
dt.month_name()           month name, e.g. 'January'
dt.quarter                quarter
dt.days_in_month          days in month
```

```python
df['month'] = df['month_date'].dt.month
df['weekday_name'] = df['month_date'].dt.day_name()
df['month_name'] = df['month_date'].dt.month_name()
```

## 30. Datetime — boolean calendar properties

```text
dt.is_month_start         is first day of month
dt.is_month_end           is last day of month
dt.is_quarter_start       first day of quarter
dt.is_quarter_end         last day of quarter
dt.is_year_start          first day of year
dt.is_year_end            last day of year
dt.is_leap_year           leap-year indicator
```

## 31. Datetime transformation

```text
dt.date                   Python date
dt.time                   Python time
dt.normalize()            reset time to midnight
dt.floor()                round datetime downward
dt.ceil()                 round datetime upward
dt.round()                round datetime normally
dt.strftime()             datetime → formatted string
dt.to_period()            timestamp → period
dt.to_pydatetime()        convert to Python datetime
```

```python
df['date'].dt.to_period('M')
df['timestamp'].dt.floor('h')
df['date'].dt.strftime('%Y-%m')
```

### Datetime arithmetic with `DateOffset` and `Timedelta`

These are top-level pandas offset/duration objects rather than `.dt` accessor methods, but they are commonly used alongside `.dt` expressions.

```python
# Calendar-aware month arithmetic
df['previous_month'] = df['date'] - pd.DateOffset(months=1)

# Fixed-duration arithmetic
df['next_week'] = df['date'] + pd.Timedelta(days=7)
```

```text
pd.DateOffset(...)        calendar-aware offset such as months/years
pd.Timedelta(...)         fixed elapsed duration such as days/hours/seconds
```

For differences between two datetime columns:

```python
df['duration'] = df['end'] - df['start']
df['duration_days'] = df['duration'].dt.days
df['duration_seconds'] = df['duration'].dt.total_seconds()
```

## 32. Time zone methods

```text
dt.tz_localize()          naive → timezone-aware
dt.tz_convert()           convert between time zones
```

```text
tz_localize()             assign timezone meaning
tz_convert()              change an existing timezone
```

## 33. Timedelta operations

```text
dt.days                   whole days
dt.seconds                remaining seconds
dt.microseconds           remaining microseconds
dt.total_seconds()        complete duration in seconds
dt.components             duration components
```

Use `.dt.total_seconds()` rather than `.dt.seconds` if durations can exceed one day.

## 34. Time-series selection

```text
at_time()                 rows at a particular clock time
between_time()            rows between clock times
first_valid_index()      first valid record
last_valid_index()       last valid record
asof()                    latest non-null observation before time
```

`asof()` is useful for market/time-series data; its exact return behavior depends on Series vs DataFrame and valid observations.

## 35. Resampling

```text
resample()                group time-series into periods
resample().sum()          sum per period
resample().mean()         mean per period
resample().agg()          arbitrary aggregation
resample().first()        first value
resample().last()         last value
resample().ffill()        forward-fill resampled periods
resample().bfill()        backward-fill
resample().interpolate()  interpolate new periods
```

```python
df.resample('ME', on='date')['value'].sum()
```

`'ME'` denotes a month-end frequency (newer Pandas naming); not the same as month-start `'MS'`.

## 36. Frequency conversion

```text
asfreq()                  convert to target frequency
to_period()               DatetimeIndex → PeriodIndex
to_timestamp()            PeriodIndex → DatetimeIndex
```

```text
resample()                group/aggregate intervals
asfreq()                  conform to different frequency
```

```python
monthly = df.set_index('date').asfreq('MS')
monthly_periods = monthly.index.to_period('M')
```

## 37. Rolling windows

```text
rolling()                 moving window
rolling().mean()          moving average
rolling().sum()           moving sum
rolling().min()           moving minimum
rolling().max()           moving maximum
rolling().std()           moving standard deviation
rolling().var()           moving variance
rolling().median()        moving median
rolling().quantile()      moving quantile
rolling().count()         valid observation count
rolling().corr()          moving correlation
rolling().cov()           moving covariance
rolling().apply()         custom rolling operation
```

```python
df['rolling_3mo'] = df['value'].rolling(3, min_periods=1).mean()
```

## 38. Expanding windows

```text
expanding()               window beginning at first row
expanding().sum()
expanding().mean()
expanding().min()
expanding().max()
expanding().std()
expanding().var()
expanding().quantile()
expanding().apply()
```

```text
rolling(10)               last 10 rows
expanding()               everything from beginning → current row
```

## 39. Exponentially weighted windows

```text
ewm()                     exponentially weighted calculation
ewm().mean()              exponential moving average
ewm().std()               exponentially weighted std
ewm().var()               exponentially weighted variance
ewm().corr()              exponentially weighted correlation
ewm().cov()               exponentially weighted covariance
```

```python
df['ewma'] = df['value'].ewm(span=10, adjust=False).mean()
```

## 40. Categorical data

```text
astype('category')        convert to categorical
cat.categories            categories
cat.codes                 integer category codes
cat.rename_categories()   rename categories
cat.reorder_categories()  change category order
cat.set_categories()      replace category definitions
cat.add_categories()      add categories
cat.remove_categories()   remove categories
cat.remove_unused_categories()
                         remove unused categories
cat.as_ordered()          make ordered
cat.as_unordered()        remove ordering
```

Fixed domain examples: `stage`, `division`, `transaction_type`, `currency`, `status`.

```python
df['stage'] = df['stage'].astype('category')
df['stage'].cat.codes
```

## 41. Binning / discretization (top-level functions)

```text
pd.cut()                 divide values into explicit bins
pd.qcut()                divide values into quantile bins
```

```text
cut()                    interval boundaries matter
qcut()                   approximately equal counts matter
```

```python
pd.cut(df['value'], bins=[0, 100, 500, 1000])
pd.qcut(df['value'], q=4, duplicates='drop')
```

## 42. Encoding / factorization

```text
pd.factorize()           values → integer codes
pd.get_dummies()         categories → indicator columns
pd.from_dummies()        dummy columns → categorical data
```

```python
codes, categories = pd.factorize(df['transaction_type'])
pd.get_dummies(df['division'], dtype=int)
```

## 43. Ordering / categorical frequencies

```text
value_counts()           frequency counts
value_counts(normalize=True)
                         proportions
unique()                 unique values
nunique()                number of unique values
mode()                   most frequent values
```

For combination frequencies:

```python
df.value_counts(['division', 'stage'])
```

Often simpler than:

```python
df.groupby(['division', 'stage']).size()
```

## 44. Data inspection

```text
head()                   first rows
tail()                   last rows
sample()                 random rows
info()                   schema + null counts + memory
describe()               descriptive statistics
memory_usage()           memory usage by column
count()                  non-null counts
nunique()                unique counts
value_counts()           frequency distribution
```

```python
df.info(memory_usage='deep')
df.describe(include='all')
df.memory_usage(deep=True)
```

## 45. Structural inspection (mainly attributes)

```text
shape                    (rows, columns)
size                     number of cells
ndim                     dimensions
columns                  column Index
index                    row Index
dtypes                   column dtypes
empty                    whether object is empty
keys()                   column labels (method)
```

## 46. Iteration

```text
items()                  iterate (column_name, Series)
iterrows()               iterate rows as Series
itertuples()             iterate rows as namedtuples
```

```text
itertuples()             usually preferable
iterrows()               convenient but slower/type-coercive
```

Prefer vectorized operations when possible; explicit row iteration is usually a last resort.

### Converting rows to Python / NumPy record structures

```text
to_dict()                DataFrame/Series → Python dictionary structures
to_dict('records')       DataFrame → list of one dict per row
to_records()             DataFrame → NumPy record array
```

`to_dict()` supports several orientations. For application code, API payload preparation, and row-oriented processing, `"records"` is especially useful:

```python
records = df.to_dict('records')

# Example result:
# [
#     {'id': 1, 'group': 'A', 'amount': 100},
#     {'id': 2, 'group': 'B', 'amount': 200},
# ]

for record in records:
    print(record['id'], record['amount'])
```

`to_records()` returns a NumPy record array whose fields correspond to DataFrame columns:

```python
records = df.to_records(index=False)

records[0]          # e.g. (1, 'A', 100)
records['amount']   # field-based access
```

```text
to_dict('records')       ordinary Python list[dict]; convenient for application/API code
to_records()             NumPy structured/record array; useful for NumPy-oriented workflows
```

`to_records(index=False)` avoids including the DataFrame index as an additional field.

## 47. Copying

```text
copy()                   copy DataFrame/Series
```

```python
df.copy()
df.copy(deep=False)
```

Modern Pandas copy-on-write changes when/why underlying data gets copied. Avoid extrapolating pre-3.0 copying behavior to all versions.

## 48. Alignment — deeply Pandas-specific

```text
align()                  align two objects on index/columns
reindex()                force object to specified labels
reindex_like()           force one object to another's structure
```

Example for comparison/testing:

```python
expected, actual = expected.align(
    actual,
    join='outer',
    axis=None,
)
```

**Caution:** alignment may insert missing labels filled with NaNs, which can conceal a structural mismatch unless explicitly checked.

## 49. Conditional replacement patterns

```text
np.where()               choose between two values/arrays by condition
np.select()              choose among multiple condition/value branches
where()                  replace where condition is False
mask()                   replace where condition is True
replace()                replace matching values
fillna()                 replace nulls
update()                 replace from another DataFrame
combine_first()          null-coalescing from another object
```

```text
condition-driven replacement
value-driven replacement
null-driven replacement
DataFrame-driven replacement
```

```python
df['amount'].mask(df['amount'] < 0, 0)
df.replace({'N/A': pd.NA})
df['value'].fillna(0)
```

### `np.where()` — vectorized if/else with NumPy

`np.where()` is a **NumPy function** commonly used to create pandas columns from conditions. Import NumPy first:

```python
import numpy as np
import pandas as pd

# Choose x when the condition is True; otherwise choose y.
np.where(condition, x, y)
```

The condition and alternatives can be arrays or scalars with compatible broadcastable shapes. With all three arguments, the result is a NumPy array.

**Example: create a category column**

```python
df = pd.DataFrame({
    'amount': [120, -30, 0, 250],
    'stage': [1, 2, 1, 3],
}, index=['a', 'b', 'c', 'd'])

df['direction'] = np.where(df['amount'] >= 0, 'credit', 'debit')
# ['credit', 'debit', 'credit', 'credit']
```

**Example: choose between calculations**

```python
df['adjusted_amount'] = np.where(
    df['stage'] == 1,
    df['amount'] * 0.9,
    df['amount'],
)
# [108.0, -30.0, 0.0, 250.0]
```

**Example: combine conditions**

```python
df['flag'] = np.where(
    (df['amount'] > 100) & (df['stage'] == 1),
    'review',
    'normal',
)
# ['review', 'normal', 'normal', 'normal']
```

Use `&` for elementwise AND, `|` for OR, and `~` for NOT. Parenthesize each comparison; Python's `and` and `or` do not combine Series elementwise.

**Comparison with pandas conditional methods**

| Operation | True positions | False positions | Result for Series input |
| --- | --- | --- | --- |
| `np.where(cond, x, y)` | Choose `x` | Choose `y` | NumPy array |
| `s.where(cond, other)` | Keep `s` | Choose `other` | Series |
| `s.mask(cond, other)` | Choose `other` | Keep `s` | Series |

```python
# These produce the same values for this example:
np.where(df['amount'] >= 0, df['amount'], 0)
df['amount'].where(df['amount'] >= 0, other=0)
df['amount'].mask(df['amount'] < 0, other=0)
# [120, 0, 0, 250]
```

Pandas methods retain labels and align Series inputs by index. `np.where()` selects by array position: it does not align Series by label. Assigning its array to a DataFrame column uses row order.

**Missing values:** explicitly choose how to handle an unknown condition. A nullable boolean condition containing `pd.NA` cannot be used directly as an ordinary NumPy boolean condition.

```python
amount = pd.Series([120, pd.NA, -30], dtype='Float64')
condition = amount.ge(0).fillna(False).to_numpy(dtype=bool)
labels = np.where(condition, 'nonnegative', 'negative or missing')
# ['nonnegative', 'negative or missing', 'negative or missing']
```

**Both alternatives are evaluated before selection.** `np.where(denominator != 0, numerator / denominator, 0)` still calculates the division first; it does not prevent division by zero. Use masked calculations or `np.divide(..., out=..., where=...)` when evaluation itself must be conditional.

**One-argument form: find positions**

```python
positions = np.where(df['amount'] < 0)
# (array([1]),)

df.iloc[positions[0]]     # row at position 1, whose index label is 'b'
```

The one-argument form returns a tuple of position arrays, one per dimension, rather than selected values or pandas index labels. NumPy recommends `np.nonzero(condition)` directly for this purpose. For filtering pandas rows, use `df.loc[df['amount'] < 0]`.

### `np.select()` — vectorized if / elif / else

`np.select()` is useful when more than two conditional branches are needed. It accepts a list of boolean conditions and a corresponding list of choices.

```python
conditions = [
    df['amount'] >= 500,
    df['amount'] >= 200,
    df['amount'] >= 100,
]

choices = [
    'very high',
    'high',
    'medium',
]

df['category'] = np.select(
    conditions,
    choices,
    default='low',
)
```

Conceptually, this corresponds to:

```python
if amount >= 500:
    category = 'very high'
elif amount >= 200:
    category = 'high'
elif amount >= 100:
    category = 'medium'
else:
    category = 'low'
```

**Condition order matters:** `np.select()` uses the **first True condition**. Put more specific / higher-priority conditions before broader ones.

```text
np.where(cond, x, y)      vectorized if / else
np.select(conds, choices) vectorized if / elif / ... / else
```

As with `np.where()`, the result is a NumPy array rather than a label-aware pandas Series. If index alignment matters, construct or assign the result carefully.

Official references:

- [NumPy `where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html)
- [NumPy `select`](https://numpy.org/doc/stable/reference/generated/numpy.select.html)

## 50. SQL-style operations

```text
query()                  SQL-WHERE-like filtering
merge()                  SQL JOIN
groupby()                SQL GROUP BY
agg()                    SQL aggregate functions
sort_values()            SQL ORDER BY
drop_duplicates()        SQL DISTINCT-like behavior
```

Actual SQL I/O:

```text
read_sql()               SQL/table → DataFrame
read_sql_query()         SQL query → DataFrame
read_sql_table()         SQL table → DataFrame
to_sql()                 DataFrame → SQL table
```

`pd.read_sql()` dispatches SQL query or table reads to the appropriate underlying behavior depending on the input.

```python
pd.read_sql('SELECT * FROM transactions', con=engine)
df.to_sql('transactions', con=engine, if_exists='append', index=False)
```

## 51. CSV / text I/O

```text
pd.read_csv()           CSV → DataFrame
pd.read_table()         delimited text → DataFrame
pd.read_fwf()           fixed-width text → DataFrame
to_csv()                DataFrame → CSV
```

Useful `read_csv()` parameters:

```text
usecols=                load subset of columns
dtype=                  force types
parse_dates=            parse date columns
index_col=              construct index
na_values=              define missing markers
nrows=                  read limited rows
skiprows=               skip rows
chunksize=              stream large files in chunks
```

```python
for chunk in pd.read_csv('transactions.csv', chunksize=100_000):
    process(chunk)
```

## 52. Excel I/O

```text
pd.read_excel()         Excel → DataFrame
to_excel()              DataFrame → Excel
pd.ExcelFile()          open workbook once
ExcelFile.parse()       parse individual sheet
pd.ExcelWriter()        write multiple sheets/files
```

```python
with pd.ExcelFile('input.xlsx') as xls:
    frames = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    control_df.to_excel(writer, sheet_name='Control', index=False)
```

## 53. Parquet / columnar formats

```text
pd.read_parquet()       Parquet → DataFrame
to_parquet()            DataFrame → Parquet
pd.read_feather()       Feather → DataFrame
to_feather()            DataFrame → Feather
pd.read_orc()           ORC → DataFrame
to_orc()                DataFrame → ORC
pd.read_iceberg()       Iceberg → DataFrame (experimental in 3.0.x)
to_iceberg()            DataFrame → Iceberg (experimental in 3.0.x)
```

## 54. JSON

```text
pd.read_json()          JSON → DataFrame
to_json()                DataFrame → JSON
pd.json_normalize()     nested JSON → flat table
```

```python
pd.json_normalize(
    data,
    record_path='transactions',
    meta=['customer_id', 'date'],
)
```

Especially useful for nested API payloads.

## 55. Other serialization formats

```text
pd.read_pickle()        Pickle → Python/Pandas object
to_pickle()             object → Pickle
pd.read_stata()         Stata → DataFrame
to_stata()              DataFrame → Stata
pd.read_sas()           SAS → DataFrame
pd.read_spss()          SPSS → DataFrame
pd.read_clipboard()     clipboard → DataFrame
to_clipboard()          DataFrame → clipboard
```

**Security:** never unpickle untrusted content; Python pickle can execute code during load.

## 56. Comparing / validating datasets

```text
equals()                exact equality
compare()               show differences
duplicated()            identify duplicates
drop_duplicates()       enforce uniqueness
isin()                  membership validation
isna()                  missingness validation
all()                   assert all conditions hold
any()                   detect any violations
```

```python
invalid = df[
    ~df['measure_type'].isin(valid_measure_types)
]
```

Or uniqueness of a Series/index:

```python
assert df['keyid'].is_unique
```

`is_unique` is a property, not an ordinary DataFrame method.

## 57. Pandas testing utilities

```text
pd.testing.assert_frame_equal()
                         assert DataFrames equal
pd.testing.assert_series_equal()
                         assert Series equal
pd.testing.assert_index_equal()
                         assert Index objects equal
pd.testing.assert_extension_array_equal()
                         assert extension arrays equal
```

```python
pd.testing.assert_frame_equal(actual, expected)
```

Prefer this in tests over:

```python
assert actual.equals(expected)
```

because it reports **how** they differ.

## 58. Row ordering / sequence utilities

```text
shift()                 previous/next row
diff()                  difference vs previous row
pct_change()            relative change
cumcount()              sequential number inside group
rank()                  ranking
sort_values()           explicit ordering
```

```python
df = (
    df.sort_values('keyid')
      .assign(
          transaction_order=lambda x:
              x.groupby('division').cumcount()
      )
)
```

## 59. MultiIndex operations

```text
set_index([...])        create MultiIndex
reset_index()           flatten MultiIndex
xs()                    select cross-section
swaplevel()             swap levels
reorder_levels()        reorder levels
droplevel()             remove levels
sort_index()            sort hierarchy
unstack()               index level → columns
stack()                 columns → index level
```

Common levels for multidimensional data:

```text
hierarchy_id
stage
measure_type
month_date
currency
```

## 60. Matrix-like operations

```text
dot()                   matrix multiplication / dot product
transpose() / T         transpose
```

```python
df.mul(weights, axis='columns')
```

Alignment can eliminate manual NumPy broadcasting.

## 61. Row/column arithmetic with alignment

```text
add(..., axis=)
sub(..., axis=)
mul(..., axis=)
div(..., axis=)
```

Subtract each column's mean:

```python
df.sub(df.mean(), axis='columns')
```

Normalize each row:

```python
df.div(df.sum(axis=1), axis='rows')
```

## 62. `eval()` — companion to `query()`

```text
eval()                  evaluate expression against columns
```

```python
df.eval('profit = revenue - cost')
```

Multiple column expressions:

```python
df.eval('''
    gross = price * quantity
    profit = gross - cost
''')
```

```text
query()                 expression → row filtering
eval()                  expression → calculations
```

## 63. Pipe-based method chains

```text
pipe()                  hand object to arbitrary function
```

```python
def clean_transactions(df):
    return df.dropna(subset=['keyid'])

def filter_cb(df):
    return df.query("division == 'CB'")

result = (
    df
    .pipe(clean_transactions)
    .pipe(filter_cb)
    .sort_values('keyid')
)
```

Use for modular, readable transformation pipelines.

## 64. Sampling

```text
sample()                random rows
sample(n=...)           fixed count
sample(frac=...)        fraction of rows
sample(weights=...)     weighted sampling
sample(random_state=...) reproducible sampling
groupby().sample()      sample independently by group
```

```python
df.sample(frac=0.1, random_state=42)
df.groupby('stage').sample(n=2, random_state=42)
```

## 65. Interpolation

```text
interpolate()           infer missing values
```

Methods/concepts:

```text
linear
time
index
values
nearest
polynomial
spline
```

```python
df['value'].interpolate(method='linear')
```

Some interpolation methods require SciPy or a suitable numeric/time index.

## 66. Frequency tables

```text
value_counts()          one/multiple dimensional frequencies
pd.crosstab()           cross-tabulation
pivot_table()           general multidimensional summary
```

```text
value_counts()          quickest
crosstab()              frequency matrix
pivot_table()           generalized grouped matrix
```

## 67. Useful top-level constructors / transforms

```text
pd.DataFrame()          construct DataFrame
pd.Series()             construct Series
pd.concat()             concatenate objects
pd.merge()              merge DataFrames
pd.to_datetime()        parse datetimes
pd.to_timedelta()       parse durations
pd.to_numeric()         parse numbers
pd.cut()                fixed bins
pd.qcut()               quantile bins
pd.factorize()          encode distinct values
pd.get_dummies()        one-hot encode
pd.crosstab()           cross-tabulation
pd.pivot_table()        pivot aggregation
pd.json_normalize()     flatten nested JSON
pd.date_range()         construct date sequence
pd.period_range()       construct period sequence
pd.timedelta_range()    construct timedelta sequence
```

## 68. Less-obvious methods worth prioritizing

```text
align()                  make two DataFrames structurally compatible
combine_first()          fill missing values from another object
compare()                expose differences between two datasets
cumcount()               generate group-local sequence numbers
ngroup()                 generate integer IDs for groups
factorize()              efficiently map values → integer IDs
xs()                     elegant MultiIndex cross-section
update()                 overwrite one DataFrame from another
reindex_like()           force one object to another's structure
idxmax() / idxmin()      retrieve location, not value, of extrema
nlargest() / nsmallest() retrieve top-N without full sort
explode()                normalize list-valued columns
json_normalize()         normalize nested API data
wide_to_long()           structured reshape of repeated columns
eval()                   column-expression calculations
pipe()                   modular DataFrame pipelines
asof()                   most recent valid observation before point
between_time()           time-of-day filtering
groupby().nth()          arbitrary positional group records
groupby().ngroup()       encode groups
groupby().cumcount()     row numbers inside groups
groupby().filter()       remove groups based on group-level rule
transform()              group result without collapsing rows
select_dtypes()          programmatic dtype-based column selection
convert_dtypes()         modern Pandas dtype inference
memory_usage()           diagnose DataFrame memory footprint
pd.testing.assert_frame_equal()
                         production-quality DataFrame test assertion
```

## Compact conceptual map — memorize operations, not an alphabet

```text
FILTER
query()
isin()
between()
where()
mask()
filter()

CREATE / MODIFY
assign()
insert()
replace()
update()

SELECT
loc[]
iloc[]
at[]
iat[]
xs()
take()

SORT
sort_values()
sort_index()
nlargest()
nsmallest()
rank()

GROUP
groupby()
agg()
transform()
apply()
filter()
cumcount()
ngroup()

RESHAPE
melt()
pivot()
pivot_table()
stack()
unstack()
explode()

COMBINE
merge()
join()
concat()
align()
combine_first()

MISSING
isna()
dropna()
fillna()
ffill()
bfill()
interpolate()

UNIQUE
duplicated()
drop_duplicates()
unique()
nunique()
value_counts()
factorize()

TIME
shift()
diff()
pct_change()
resample()
asfreq()
rolling()
expanding()
ewm()

STRINGS
str.contains()
str.extract()
str.replace()
str.split()
str.cat()
str.strip()

DATETIME
dt.year
dt.month
dt.day_name()
dt.month_name()
dt.floor()
dt.strftime()
dt.to_period()

TYPES
astype()
convert_dtypes()
select_dtypes()
to_numeric()
to_datetime()

FUNCTIONS
map()
apply()
agg()
transform()
pipe()
np.where()
np.select()

CONVERT / RECORDS
to_dict()
to_dict('records')
to_records()

INSPECT
info()
describe()
memory_usage()

COMPARE / TEST
equals()
compare()
pd.testing.assert_frame_equal()

I/O
read_csv()
read_excel()
read_parquet()
read_sql()
read_json()
to_csv()
to_excel()
to_parquet()
to_sql()
to_json()
```

### Recommended priority list for advanced data/transaction workflows

`align`, `transform`, `cumcount`, `ngroup`, `xs`, `combine_first`, `update`, `compare`, `factorize`, `select_dtypes`, `eval`, `pipe`, `groupby().filter`, `groupby().nth`, `explode`, `pd.testing.assert_frame_equal()`.

They often replace procedural Python with concise, readable, vectorized operations.

### Official references

- [Pandas API reference](https://pandas.pydata.org/docs/reference/)
- [Pandas GroupBy API](https://pandas.pydata.org/docs/reference/groupby.html)
- [Pandas Series string accessor](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.html)
- [Pandas input/output](https://pandas.pydata.org/docs/reference/io.html)
- [Series.map](https://pandas.pydata.org/docs/reference/api/pandas.Series.map.html)
- [Series.str.fullmatch](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.fullmatch.html)
- [Series.str.extract](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html)
- [Series.str.zfill](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.zfill.html)
- [pd.read_sql](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html)
