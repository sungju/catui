///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version 3.9.0 Aug  6 2020)
// http://www.wxformbuilder.org/
//
// PLEASE DO *NOT* EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

FrameCrash::FrameCrash( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );

	wxBoxSizer* bs_main;
	bs_main = new wxBoxSizer( wxVERTICAL );

	rt_main_output = new wxRichTextCtrl( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, 0|wxVSCROLL|wxHSCROLL|wxNO_BORDER|wxWANTS_CHARS );
	bs_main->Add( rt_main_output, 1, wxEXPAND | wxALL, 5 );

	tc_command_input = new wxTextCtrl( this, wxID_ANY, wxEmptyString, wxDefaultPosition, wxDefaultSize, wxTE_PROCESS_ENTER );
	bs_main->Add( tc_command_input, 0, wxALL|wxEXPAND, 5 );


	this->SetSizer( bs_main );
	this->Layout();

	this->Centre( wxBOTH );

	// Connect Events
	this->Connect( wxEVT_CHAR_HOOK, wxKeyEventHandler( FrameCrash::OnCharHook ) );
	this->Connect( wxEVT_KEY_DOWN, wxKeyEventHandler( FrameCrash::FrameCrashOnKeyDown ) );
	tc_command_input->Connect( wxEVT_COMMAND_TEXT_ENTER, wxCommandEventHandler( FrameCrash::OnEnter ), NULL, this );
}

FrameCrash::~FrameCrash()
{
	// Disconnect Events
	this->Disconnect( wxEVT_CHAR_HOOK, wxKeyEventHandler( FrameCrash::OnCharHook ) );
	this->Disconnect( wxEVT_KEY_DOWN, wxKeyEventHandler( FrameCrash::FrameCrashOnKeyDown ) );
	tc_command_input->Disconnect( wxEVT_COMMAND_TEXT_ENTER, wxCommandEventHandler( FrameCrash::OnEnter ), NULL, this );

}
