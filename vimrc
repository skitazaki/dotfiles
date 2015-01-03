" Call dotvim
source ~/.vim/dotvim.vim

if has("user_commands")
  filetype off
  set rtp+=~/.vim/bundle/vundle/
  call vundle#rc()
  let g:vundles=['general', 'programming', 'python', 'javascript', 'html', 'misc', 'go']
  "let g:vundles=['general', 'programming']
  let g:neocomplcache_enable_at_startup = 1
  " Load 'vundles'
  " source ~/.vim/vundles.vim
  " Vundle itself
  Plugin 'gmarik/vundle'
  " Add extra bundles here...
  Plugin 'scrooloose/nerdtree'
  " Plugin 'chriskempson/base16-vim'
  " Plugin 'altercation/vim-colors-solarized'
  Plugin 'bling/vim-airline'
  Plugin 'tyru/caw.vim.git'
  nmap <Leader>c <Plug>(caw:i:toggle)
  vmap <Leader>c <Plug>(caw:i:toggle)
  Plugin 'scrooloose/syntastic'
  Plugin 'klen/python-mode'
  Plugin 'fatih/vim-go'
  Plugin 'nathanaelkane/vim-indent-guides'
  let g:indent_guides_enable_on_vim_startup = 1
  let g:indent_guides_guide_size = 1
  let g:indent_guides_auto_colors = 0
  autocmd VimEnter,Colorscheme * :hi IndentGuidesEven ctermbg=darkgrey guibg=darkgrey ctermbg=0
endif
syntax enable
set t_Co=256
set background=dark
" let base16colorspace=256
" colorscheme base16-solarized
colorscheme desert
" colorscheme solarized

" Share yank buffer in Vim and clipboard in OS.
" set clipboard=unnamed,autoselect

" Japanese settings, default is `UTF-8'
set fileencodings=iso-2022-jp,cp932,sjis,euc-jp,utf-8
set fileformats=unix,dos,mac
set termencoding=utf-8

" Key mapping
nmap ;          :w<CR>
nmap <C-A>      ggyG''<Esc>
"nmap <C-H>      :help<Space>
"nmap <C-I>      :e<Space>
"nmap <C-J>      :sp<Space>
"nmap <C-K>      :w<CR>
nmap <C-N>      :tabn<CR>
nmap <C-O>      :tabnew<Space>
nmap <C-P>      :tabp<CR>
nmap <Space>    :tabn<CR>
nmap <Return>   :w<CR>:sh<CR>
nmap <Esc><Esc> :nohlsearch<CR>

" ftplugin
let g:changelog_username="Kitazaki <skitazaki[at]gmail.com>"

