" Japanese settings, default is `UTF-8'
set encoding=utf-8
set fileencodings=utf-8,iso-2022-jp,euc-jp,cp932
set termencoding=utf-8
set fileformats=unix,dos

set number
set ruler
set wildmenu
set paste
set clipboard+=unnamed
set backspace=indent,eol,start

set modeline
set modelines=5

set laststatus=2
set statusline=%<%f\ %m%r%{'['.(&fenc!=''?&fenc:&enc).']['.&ff.']['.&ft.']'}%=%l/%L,%v
set tabline=%!MyTabLine()

" Programmer settings
syntax on
filetype plugin on
set expandtab
set incsearch hlsearch
set backup
set cindent
set showmatch
set shiftwidth=4 tabstop=4 softtabstop=4
set textwidth=0
if exists('&colorcolumn')
    " set colorcolumn=+1
    " autocmd FileType sh,c,cpp,vim,python,haskell,javascript setlocal textwidth=80
endif
set foldlevel=0
set tags=.tags
set commentstring=\ #\ %s

" Key mapping
nmap ;          :w<CR>
nmap <C-A>      ggyG''<Esc>
nmap <C-H>      :help<Space>
nmap <C-I>      :e<Space>
nmap <C-J>      :sp<Space>
nmap <C-K>      :w<CR>
nmap <C-N>      :tabn<CR>
nmap <C-O>      :tabnew<Space>
nmap <C-P>      :tabp<CR>
nmap <Space>    :tabn
nmap <Return>   :w<CR>:sh<CR>
nmap <Esc><Esc> :nohlsearch<CR>

" <Leader> is backslash on default.
" <http://stackoverflow.com/questions/1764263/what-is-the-leader-in-a-vimrc-file>
" `dumbbuf plugin
let g:dumbbuf_hotkey = '<Leader>b'

" ftplugin
let g:changelog_username="Kitazaki <skitazaki[at]gmail.com>"

function MyTabLine()
  let s = ''
  for i in range(tabpagenr('$'))
    " select the highlighting
    if i + 1 == tabpagenr()
      let s .= '%#TabLineSel#'
    else
      let s .= '%#TabLine#'
    endif

    " set the tab page number (for mouse clicks)
    let s .= '%' . (i + 1) . 'T'

    " the label is made by MyTabLabel()
    let s .= ' %{MyTabLabel(' . (i + 1) . ')} '
  endfor

  " after the last tab fill with TabLineFill and reset tab page nr
  let s .= '%#TabLineFill#%T'

  " right-align the label to close the current tab page
  if tabpagenr('$') > 1
    let s .= '%=%#TabLine#%999Xclose'
  endif

  return s
endfunction
function MyTabLabel(n)
  let buflist = tabpagebuflist(a:n)
  let winnr = tabpagewinnr(a:n)
  return bufname(buflist[winnr - 1])
endfunction
